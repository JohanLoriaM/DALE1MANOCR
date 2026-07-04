
declare const process: {
  env: {
    NUXT_PUBLIC_API_BASE?: string
    [key: string]: string | undefined
  }
}

export default defineNuxtConfig({
  
  compatibilityDate: '2024-04-03',
  modules: [
    '@nuxtjs/tailwindcss'
  ],
  
  devtools: { enabled: true },


  runtimeConfig: {
    public: {
      
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:5000/api'
    }
  }
})