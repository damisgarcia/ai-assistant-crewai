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
  <div class="w-full max-w-2xl mx-auto">
    <MDC
      v-if="message.sender_type === 'ai-assistant'"
      :value="sampleMakdown"
      tag="article"
      class="prose dark:prose-invert lg:prose-xl"
    />
    <div v-else class="flex flex-col gap-2">
      <div>
        {{ message.content }}
      </div>
      <time>{{ message.created_at }}</time>
    </div>
  </div>
</template>
