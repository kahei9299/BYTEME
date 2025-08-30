export default {
  entry: './src/App.tsx',
  output: {
    path: './dist',
  },
  devServer: {
    port: 3000,
    host: '0.0.0.0',
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.jsx', '.js'],
  },
  typescript: {
    configFile: './tsconfig.json',
  },
};