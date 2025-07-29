<script lang="ts" setup>
const container = useTemplateRef("container");

function scrollToBottom() {
  if (container.value) {
    container.value.scrollTop = container.value.scrollHeight;
  }
}

onMounted(() => {
  scrollToBottom();
});
</script>

<template>
  <div
    ref="container"
    class="flex flex-col flex-1 gap-4 pt-4 pb-10 relative overflow-y-auto"
  >
    <slot></slot>
  </div>
</template>
