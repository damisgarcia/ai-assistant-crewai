<script lang="ts" setup>
const { create, fetchAll } = useConversation();

const { data: conversations, refresh } = await useAsyncData(
  "conversations",
  async () => {
    return await fetchAll();
  }
);

const conversationAsk = ref("");

async function onAsk(content: string) {
  await create({ title: content });
  refresh();
}
</script>

<template>
  <div class="grid h-screen grid-cols-5">
    <layout-aside>
      <suspense>
        <conversation-list
          v-if="conversations"
          :conversations="conversations"
        />
        <template #fallback>
          <div class="text-sm">Carregando...</div>
        </template>
      </suspense>
    </layout-aside>
    <layout-content class="col-span-4">
      <ConversationWelcome class="flex-1" />
      <ConversationInput v-model="conversationAsk" @submit="onAsk" />
    </layout-content>
  </div>
</template>
