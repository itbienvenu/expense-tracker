<template>
  <div v-if="notifications.length > 0" class="notification-container">
    <transition-group name="fade" tag="div">
      <div 
        v-for="notification in notifications" 
        :key="notification.id"
        class="alert alert-dismissible fade show mb-2"
        :class="`alert-${notification.type}`"
        role="alert"
      >
        {{ notification.message }}
        <button type="button" class="btn-close" @click="removeNotification(notification.id)" aria-label="Close"></button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const notifications = ref([]);
let nextId = 0;

const addNotification = (message, type = 'success', timeout = 5000) => {
  const newId = nextId++;
  const newNotification = {
    id: newId,
    message,
    type,
  };
  notifications.value.push(newNotification);

  if (timeout) {
    setTimeout(() => {
      removeNotification(newId);
    }, timeout);
  }
};

const removeNotification = (id) => {
  notifications.value = notifications.value.filter(n => n.id !== id);
};

onMounted(() => {
  window.addNotification = addNotification;
});

onUnmounted(() => {
  delete window.addNotification;
});

</script>

<style scoped>
.notification-container {
  position: fixed;
  top: 70px; 
  right: 15px;
  width: 350px;
  z-index: 1050;
}


.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>