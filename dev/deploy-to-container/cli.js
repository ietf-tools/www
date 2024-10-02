#!/usr/bin/env node

import Docker from 'dockerode'
import yargs from 'yargs/yargs'
import { hideBin } from 'yargs/helpers'
import slugify from 'slugify'
import { nanoid } from 'nanoid'
import { setTimeout } from 'timers/promises'
import path from 'path'

async function main () {
  const basePath = process.cwd()
  const argv = yargs(hideBin(process.argv)).argv

  // Parse branch argument
  let branch = argv.branch
  if (!branch) {
    throw new Error('Missing --branch argument!')
  }
  if (branch.indexOf('/') >= 0) {
    branch = branch.split('/').slice(1).join('-')
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

  // Build latest DB image
  console.info('Building latest DB docker image...')
  const dbImageBuildStream = await dock.buildImage({
    context: process.cwd(),
    src: [
      'docker/db.Dockerfile',
      'docker/scripts/db-import.sh',
      'docker/database/ietfwww.dump'
    ]
  }, {
    dockerfile: 'docker/db.Dockerfile',
    t: 'ws-db:latest'
  })
  await new Promise((resolve, reject) => {
    dock.modem.followProgress(dbImageBuildStream, (err, res) => err ? reject(err) : resolve(res))
  })
  console.info('Building latest DB docker image successfully.')

  // Pull latest memcached image
  console.info('Pulling latest memcached image...')
  const mcImagePullStream = await dock.pull(`memcached:latest`)
  await new Promise((resolve, reject) => {
    dock.modem.followProgress(mcImagePullStream, (err, res) => err ? reject(err) : resolve(res))
  })
  console.info('Pulled latest memcached image.')

  // Pull latest WWW Base image
  console.info('Pulling latest WWW branch docker image...')
  const appImagePullStream = await dock.pull(`ghcr.io/ietf-tools/www:${argv.appversion}`)
  await new Promise((resolve, reject) => {
    dock.modem.followProgress(appImagePullStream, (err, res) => err ? reject(err) : resolve(res))
  })
  console.info('Pulled latest WWW branch docker image.')

  // Terminate existing containers
  console.info('Ensuring existing containers with same name are terminated...')
  const containers = await dock.listContainers({ all: true })
  for (const container of containers) {
    if (
      container.Names.includes(`/ws-db-${branch}`) ||
      container.Names.includes(`/ws-app-${branch}`) ||
      container.Names.includes(`/ws-mc-${branch}`)
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
    Image: 'ws-db:latest',
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

  // Create memcached container
  console.info(`Creating memcached docker container... [ws-mc-${branch}]`)
  const mcContainer = await dock.createContainer({
    Image: 'memcached:latest',
    name: `ws-mc-${branch}`,
    Hostname: `ws-mc-${branch}`,
    HostConfig: {
      NetworkMode: 'shared',
      RestartPolicy: {
        Name: 'unless-stopped'
      }
    }
  })
  await mcContainer.start()
  console.info('Created and started memcached docker container successfully.')

  // Create App container
  console.info(`Creating app docker container... [ws-app-${branch}]`)
  const appContainer = await dock.createContainer({
    Image: `ghcr.io/ietf-tools/www:${argv.appversion}`,
    name: `ws-app-${branch}`,
    Hostname: `ws-app-${branch}`,
    Env: [
      // `LETSENCRYPT_HOST=${hostname}`,
      `VIRTUAL_HOST=${hostname}`,
      `VIRTUAL_PORT=80`,
      `DJANGO_SETTINGS_MODULE=ietf.settings.production`,
      `PGHOST=ws-db-${branch}`,
      `PGDATABASE=ietfwww`,
      `PGUSER=postgres`,
      `PGPASSWORD=password`,
      `SECRET_KEY=${nanoid(36)}`,
      `CACHE_DEFAULT=ws-mc-${branch}:11211`,
      `CACHE_SESSIONS=ws-mc-${branch}:11211`,
      `ALLOWED_HOSTS=${hostname}`,
      `CSRF_TRUSTED_ORIGINS=https://*.dev.ietf.org`,
      `PRIMARY_HOST=${hostname}`
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
  await setTimeout(5000)
  console.info('Created app container successfully.')

  // Inject media archive into the App container
  console.info('Injecting media archive into app container...')
  const tgzPath = path.join(basePath, 'media.tgz')
  await appContainer.putArchive(tgzPath, { path: '/app/media' })
  console.info(`Imported media files into app container successfully.`)

  // Start app container
  console.info('Starting app container...')
  await appContainer.start()
  console.info('Started app container successfully.')

  // Send deploy command in App container
  console.info('Running deploy script in app container...')
  const appDeployExecHandle = await appContainer.exec({
    Cmd: ['/app/deploy.sh'],
    AttachStdout: true,
    AttachStderr: true
  })
  await appDeployExecHandle.start()
  let appDeployCounter = 1
  while (appDeployCounter > 0) {
    const execState = await appDeployExecHandle.inspect()
    if (!execState.Running) {
      appDeployCounter = 0
    } else if (appDeployCounter > 60) {
      console.error('Deploy script failed to complete before timeout. Terminating...')
      process.exit(1)
    } else {
      await setTimeout(5000)
      console.info(`Waiting for deploy script in app container to complete... (${appDeployCounter * 5}s / 300s max)`)
      appDeployCounter++
    }
  }
  console.info('Deploy script completed.')

  // Restart App Container
  console.info('Restarting app container...')
  await appContainer.restart()
  console.info('Restarted app container successfully.')

  process.exit(0)
}

main()
