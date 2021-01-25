const packageJson = require('./package.json');
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const FixPaths = require('./webpack.fix-django-paths');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const postcssNormalize = require('postcss-normalize');
const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');

module.exports = (env, options) => {
    return {
        mode: options.mode,
        devtool:
            options.mode !== 'production' ? 'inline-source-map' : undefined,
        entry: './ietf/static_src/index.js',
        output: {
            filename: '[name].js',
            path: path.resolve(__dirname, 'ietf/static/dist'),
        },
        resolve: {
            extensions: ['.tsx', '.ts', '.js'],
        },
        plugins: [
            new HtmlWebpackPlugin({
                title: 'Output Management',
                template: path.resolve(
                    __dirname,
                    'ietf/templates_src/base.html',
                ),
                filename: path.resolve(__dirname, 'ietf/templates/base.html'),
            }),
            new FixPaths(),
            new MiniCssExtractPlugin({
                // Options similar to the same options in webpackOptions.output
                // both options are optional
                filename: '[name].css',
                chunkFilename: '[id].css',
            }),
        ],
        module: {
            rules: [
                {
                    test: /\.tsx?$/,
                    exclude: /(node_modules)/,
                    use: [
                        {
                            loader: 'babel-loader',
                        },
                    ],
                },
                {
                    test: /\.scss$/,
                    use: [
                        {
                            loader: MiniCssExtractPlugin.loader,
                        },
                        {
                            loader: 'css-loader', // translates CSS into CommonJS
                            options: {
                                sourceMap: options.mode === 'development',
                                importLoaders: 2,
                            },
                        },
                        {
                            loader: 'postcss-loader',
                            options: {
                                sourceMap: options.mode === 'development',
                                ident: 'postcss',
                                plugins: () => [
                                    postcssNormalize,
                                    autoprefixer,
                                    cssnano,
                                ],
                            },
                        },
                        'sass-loader', // compiles Sass to CSS
                    ],
                },
                // {
                //     test: /\.svg$/,
                //     use: ['svgo-loader'],
                // },
                {
                    test: /\.woff|woff2|otf|eot|ttf|svg$/,
                    loader: 'file-loader',
                },
            ],
        },
    };
};
