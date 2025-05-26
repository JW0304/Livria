<script setup>
import { computed } from "vue";

const props = defineProps({
  page: Number,
  total: Number,
  perPage: {
    type: Number,
    default: 12,
  },
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
