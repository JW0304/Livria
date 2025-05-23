<template>
  <div class="pagination">
    <button @click="goTo(page - 1)" :disabled="page <= 1">◀</button>

    <button
      v-for="p in visiblePages"
      :key="p"
      :class="{ active: p === page }"
      @click="goTo(p)"
    >
      {{ p }}
    </button>

    <button @click="goTo(page + 1)" :disabled="page >= totalPages">▶</button>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  page: Number, // 현재 페이지
  total: Number, // 전체 아이템 개수
  perPage: (Number = 12), // 한 페이지당 아이템 수
});
const emit = defineEmits(["change"]);

const totalPages = computed(() => Math.ceil(props.total / props.perPage));

const visiblePages = computed(() => {
  const maxPages = 5;
  const pages = [];
  const start = Math.max(1, props.page - Math.floor(maxPages / 2));
  const end = Math.min(start + maxPages - 1, totalPages.value);
  for (let i = start; i <= end; i++) pages.push(i);
  return pages;
});

function goTo(p) {
  if (p >= 1 && p <= totalPages.value && p !== props.page) {
    emit("change", p);
  }
}
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin: 2rem 0;
}
button {
  padding: 0.5rem 1rem;
  background: #222;
  color: white;
  border: none;
  cursor: pointer;
}
button.active {
  background: #e91e63;
  font-weight: bold;
}
button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
</style>
