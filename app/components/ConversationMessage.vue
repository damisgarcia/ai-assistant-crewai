<script lang="ts" setup>
defineProps({
  message: {
    type: Object as () => any,
    required: true,
  },
});
</script>

<template>
  <div class="w-full max-w-2xl mx-auto">
    <div v-if="message.sender_type == 'ai_agent'" class="flex flex-col gap-2">
      <MDC
        tag="article"
        :value="message.content"
        class="prose prose-lg dark:prose-invert"
      />
      <time>{{ message.created_at }}</time>
    </div>
    <div v-else class="flex flex-col gap-2">
      <div>
        {{ message.content }}
      </div>
      <time>{{ message.created_at }}</time>
    </div>
  </div>
</template>
