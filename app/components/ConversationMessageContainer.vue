<script lang="ts" setup>
const container = useTemplateRef("container");

const props = defineProps({
  ready: {
    type: Boolean,
    default: true,
  },
});

watch(
  () => props.ready,
  (newValue) => {
    setTimeout(() => {
      if (newValue && container.value) {
        // Scroll to the bottom when ready
        scrollToBottom();
      }
    }, 800);
  },
  { immediate: true }
);

onMounted(scrollToBottom);

function scrollToBottom() {
  if (container.value) {
    container.value.scrollTop = container.value.scrollHeight;
  }
}
</script>

<template>
  <div
    ref="container"
    class="flex flex-col flex-1 gap-4 pt-4 pb-10 relative overflow-y-auto transition-opacity delay-700 duration-700"
    :class="{ 'opacity-0': !ready }"
  >
    <slot></slot>
  </div>
</template>
