<script lang="ts" setup>
defineProps({
  conversations: {
    type: Array as () => { id: string; title: string }[],
    required: true,
  },
});
</script>

<template>
  <div>
    <div class="text-lg font-medium mb-6">Chats</div>
    <div class="flex flex-col gap-4">
      <div class="mb-4">
        <UButton
          size="lg"
          color="primary"
          variant="outline"
          as="router-link"
          to="/"
          icon="ic:twotone-article"
        >
          New Chat
        </UButton>
      </div>
      <div v-for="c in conversations" :key="c.id">
        <UButton
          size="lg"
          color="neutral"
          variant="ghost"
          as="router-link"
          :to="{ name: 'conversations-id', params: { id: c.id } }"
          active-class="bg-gray-200 dark:bg-gray-700"
        >
          {{ c.title }}
        </UButton>
      </div>
    </div>
  </div>
</template>
