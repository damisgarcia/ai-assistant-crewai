<script lang="ts" setup>
defineProps({
  visible: {
    type: Boolean,
    required: true,
  },
});
</script>

<template>
  <div class="absolute inset-0 flex -mt-0">
    <UProgress
      animation="swing"
      class="w-full rounded-none duration-1000 delay-500"
      :class="{ 'opacity-0': !visible }"
    />
  </div>
</template>
