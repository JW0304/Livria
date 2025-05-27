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

<style lang="scss" scoped>
/* Footer 스타일 */
footer {
  background: linear-gradient(
    to bottom,
    transparent,
    #000000
  ); /* 위쪽은 투명, 아래쪽은 검정색 */
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
</style>
