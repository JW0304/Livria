<template>
  <footer>
    <div class="footer-content">
      <div class="left">
        <p>© 2025 Livria</p>
        <p>모든 권리 보유.</p>
      </div>
      <div class="right">
        <p>Livria</p>
      </div>
    </div>
  </footer>
</template>

<script setup></script>

<style scoped lang="scss">
footer {
  /* 투명 배경으로 설정해 body 그라데이션이 그대로 보이게 처리 */
  background: transparent;
  padding: 20px;
  color: rgb(148, 148, 148);
  text-align: center;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .left {
    font-size: 14px;
  }

  .right {
    font-size: 16px;
    font-weight: bold;
  }
}

/* 푸터 전용 키프레임 (필요 시 사용 가능) */
@keyframes gradientBG {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>
