<template>
  <div>
    <iframe 
      id="iframe"
      width="600" 
      height="400" 
      title="Api Documentation Cite"
    ></iframe>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';

const API_DOC_URL = import.meta.env.VITE_API_DOCUMENTATION_URL;

onMounted(() => {
  const iframe = document.getElementById("iframe");
  iframe.setAttribute('src', `${API_DOC_URL}/docs/api/authentication`);
  console.log(iframe);
});
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

iframe {
  display: block;
  height: 100vh;
  width: 100vw; 
  border: none; 
}
</style>