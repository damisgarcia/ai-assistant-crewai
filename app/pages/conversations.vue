<script lang="ts" setup>
const { fetchAll } = useConversation();

const { data: conversations } = await useAsyncData(
  "conversations",
  async () => {
    return await fetchAll();
  }
);
</script>

<template>
  <div class="grid min-h-screen max-h-screen overflow-hidden grid-cols-5">
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
    <client-only>
      <suspense>
        <ws-conversation-provider>
          <NuxtPage />
        </ws-conversation-provider>
      </suspense>
    </client-only>
  </div>
</template>
