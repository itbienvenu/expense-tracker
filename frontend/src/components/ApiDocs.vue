<template>
  <div id="swagger-ui" />
</template>

<script>
import SwaggerUI from 'swagger-ui-dist/swagger-ui-es-bundle.js';
import 'swagger-ui-dist/swagger-ui.css';

export default {
  name: 'ApiDocs',
  mounted() {
    SwaggerUI({
      dom_id: '#swagger-ui',
      url: 'http://localhost:8000/openapi.json',
      presets: [
        SwaggerUI.presets.apis,
      ],
      layout: 'BaseLayout',
    });
  },
};
</script>

<style scoped>
#swagger-ui {
  min-height: 90vh;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  padding: 1rem;
}
</style>
