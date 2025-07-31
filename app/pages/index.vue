<script lang="ts" setup>
const { create, fetchAll } = useConversation();
const { setPendingMessage } = useMessageStore();

const { data: conversations, refresh } = await useAsyncData(
  "conversations",
  async () => {
    return await fetchAll();
  }
);

const conversationAsk = ref("");

async function onAsk(content: string) {
  const result = await create({ title: content });
  await refresh();

  // definindo a mensagem pendente
  // para que o Trend possa enviar quando estiver conectado
  setPendingMessage(content);

  nextTick(() => {
    if (result) {
      navigateTo({ name: "conversations-id", params: { id: result.id } });
    }
  });
}
</script>

<template>
  <div class="grid h-screen grid-cols-5">
    <layout-aside>
      <suspense>
        <conversation-list
          v-if="conversations"
          :conversations="conversations"
          @destroy="refresh"
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
