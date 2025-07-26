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
      <div v-for="c in conversations" :key="c.id">
        <UButton size="lg" color="neutral" variant="ghost">
          {{ c.title }}
        </UButton>
      </div>
    </div>
  </div>
</template>
