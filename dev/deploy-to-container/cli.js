#!/usr/bin/env node

import Docker from 'dockerode'
import yargs from 'yargs/yargs'
import { hideBin } from 'yargs/helpers'
import slugify from 'slugify'
import { nanoid } from 'nanoid'

async function main () {
  const argv = yargs(hideBin(process.argv)).argv

  // Parse branch argument
  let branch = argv.branch
  if (!branch) {
    throw new Error('Missing --branch argument!')
  }
  if (branch.indexOf('/') >= 0) {
    branch = branch.split('/')[1]
  }
  branch = slugify(branch, { lower: true, strict: true })
  if (branch.length < 1) {
    throw new Error('Branch name is empty!')
  }
  console.info(`Will use branch name "${branch}"`)

  // Parse domain argument
  const domain = argv.domain
  if (!domain) {
    throw new Error('Missing --domain argument!')
  }
  const hostname = `ws-${branch}.${domain}`
  console.info(`Will use hostname "${hostname}"`)

  // Connect to Docker Engine API
  console.info('Connecting to Docker Engine API...')
  const dock = new Docker()
  await dock.ping()
  console.info('Connected to Docker Engine API.')

  // Pull latest DB image
  console.info('Pulling latest DB docker image...')
  const dbImagePullStream = await dock.pull('ghcr.io/ietf-tools/wagtail_website-db:latest')
  await new Promise((resolve, reject) => {
    dock.modem.followProgress(dbImagePullStream, (err, res) => err ? reject(err) : resolve(res))
  })
  console.info('Pulled latest DB docker image successfully.')
  
  // Pull latest Wagtail_website Base image
  console.info('Pulling latest Wagtail_website branch docker image...')
  const appImagePullStream = await dock.pull(`ghcr.io/ietf-tools/wagtail_website:${branch}`)
  await new Promise((resolve, reject) => {
    dock.modem.followProgress(appImagePullStream, (err, res) => err ? reject(err) : resolve(res))
  })
  console.info('Pulled latest Wagtail_website branch docker image.')

  // Terminate existing containers
  console.info('Ensuring existing containers with same name are terminated...')
  const containers = await dock.listContainers({ all: true })
  for (const container of containers) {
    if (
      container.Names.includes(`/ws-db-${branch}`) ||
      container.Names.includes(`/ws-app-${branch}`)
      ) {
      console.info(`Terminating old container ${container.Id}...`)
      const oldContainer = dock.getContainer(container.Id)
      if (container.State === 'running') {
        await oldContainer.stop({ t: 5 })
      }
      await oldContainer.remove({
        force: true,
        v: true
      })
    }
  }
  console.info('Existing containers with same name have been terminated.')

  // Get shared docker network
  console.info('Querying shared docker network...')
  const networks = await dock.listNetworks()
  if (!networks.some(n => n.Name === 'shared')) {
    console.info('No shared docker network found, creating a new one...')
    await dock.createNetwork({
      Name: 'shared',
      CheckDuplicate: true
    })
    console.info('Created shared docker network successfully.')
  } else {
    console.info('Existing shared docker network found.')
  }

  // Create DB container
  console.info(`Creating DB docker container... [ws-db-${branch}]`)
  const dbContainer = await dock.createContainer({
    Image: 'ghcr.io/ietf-tools/wagtail_website/wagtail_website-db:latest',
    name: `ws-db-${branch}`,
    Hostname: `ws-db-${branch}`,
    HostConfig: {
      NetworkMode: 'shared',
      RestartPolicy: {
        Name: 'unless-stopped'
      }
    }
  })
  await dbContainer.start()
  console.info('Created and started DB docker container successfully.')

  // Create App container
  console.info(`Creating Wagtail_website docker container... [ws-app-${branch}]`)
  const appContainer = await dock.createContainer({
    Image: `ghcr.io/ietf-tools/wagtail_website:${branch}`,
    name: `ws-app-${branch}`,
    Hostname: `ws-app-${branch}`,
    Env: [
      `LETSENCRYPT_HOST=${hostname}`,
      `VIRTUAL_HOST=${hostname}`,
      `VIRTUAL_PORT=8001`,
      `DATABASE_URL=postgres://postgres:password@ws-db-${branch}/app`,
      `APP_SECRET_KEY=${nanoid(36)}`
    ],
    Labels: {
      appversion: `${argv.appversion}` ?? '0.0.0',
      commit: `${argv.commit}` ?? 'unknown',
      ghrunid: `${argv.ghrunid}` ?? '0',
      hostname
    },
    HostConfig: {
      NetworkMode: 'shared',
      RestartPolicy: {
        Name: 'unless-stopped'
      }
    }
  })
  await appContainer.start()
  console.info('Created and started Wagtail_website container started successfully.')

  process.exit(0)
}

main()
