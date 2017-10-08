var path = require('path')
var webpack = require('webpack')
var autoprefixer = require('autoprefixer');
var precss = require('precss');


module.exports = {
    devtool: 'cheap-module-eval-source-map',
    entry: [
        // 'webpack-hot-middleware/client',
        'babel-polyfill',
        './src/index'
    ],
    output: {
        path: path.join(__dirname, 'dist'),
        filename: 'bundle.js',
        publicPath: '/static/'
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                enforce: 'pre',
                loader: 'eslint-loader'
            },
            {
                loader: 'react-hot-loader',
                include: [path.resolve(__dirname, 'src')],
                test: /\.js$/,
                options: {
                    plugins: ['transform-runtime']
                }
            },
            {
                loader: 'babel-loader',
                include: [path.resolve(__dirname, 'src')],
                test: /\.js$/,
                options: {
                    plugins: ['transform-runtime']
                }
            },
            {
                test: /\.css$/,
                loader: 'style-loader!css-loader'
            }

        ],
    },
    plugins: [
        new webpack.optimize.OccurrenceOrderPlugin(),
        new webpack.HotModuleReplacementPlugin()
    ]
}
