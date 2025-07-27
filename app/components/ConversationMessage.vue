<script lang="ts" setup>
import { sampleMakdown } from "@/utils/content";

defineProps({
  message: {
    type: Object as () => any,
    required: true,
  },
});
</script>

<template>
  <div class="mx-auto">
    <MDC
      :value="sampleMakdown"
      tag="article"
      class="prose dark:prose-invert lg:prose-xl"
    />
  </div>
</template>
