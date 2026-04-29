<template>
  <div class="container">
    <h1>抱闸器多传感器 AI 监测系统</h1>
    <div class="card">
      <h3>实时传感器输入</h3>
      <div class="input-group">
        <label>温度 (℃):</label> <input type="number" v-model="form.temp">
        <label>振动 (mm/s):</label> <input type="number" v-model="form.vib">
        <label>间隙 (mm):</label> <input type="number" v-model="form.gap">
      </div>
      <button @click="getDiagnosis" :disabled="loading">开始 AI 诊断</button>
    </div>

    <div v-if="result" class="result-card" :class="statusClass">
      <h2>诊断结果: {{ result.status }}</h2>
      <p><strong>磨损水平:</strong> {{ result.wear_level }}%</p>
      <p><strong>分析:</strong> {{ result.analysis }}</p>
      <p><strong>建议操作:</strong> {{ result.action }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';

const form = ref({ temp: 45.0, vib: 1.5, gap: 1.2 });
const result = ref(null);
const loading = ref(false);

const statusClass = computed(() => {
  if (!result.value) return '';
  if (result.value.status === '危险') return 'danger';
  if (result.value.status === '预警') return 'warning';
  return 'normal';
});

const getDiagnosis = async () => {
  loading.value = true;
  try {
    const res = await axios.post('http://localhost:8080/api/brake/diagnose', form.value);
    result.value = res.data;
  } catch (e) {
    alert('请求失败，请检查后端服务是否启动');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.container { max-width: 800px; margin: 0 auto; font-family: sans-serif; }
.card { border: 1px solid #ccc; padding: 20px; border-radius: 8px; }
.input-group { display: flex; gap: 10px; margin-bottom: 20px; }
.result-card { margin-top: 20px; padding: 20px; border-radius: 8px; border-left: 10px solid; }
.normal { background: #e6fffa; border-left-color: #38b2ac; }
.warning { background: #fffaf0; border-left-color: #ed8936; }
.danger { background: #fff5f5; border-left-color: #e53e3e; }
</style>
