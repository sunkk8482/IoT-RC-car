<script setup>
import { ref } from "vue";
import io from "socket.io-client"
import VueApexCharts from "vue3-apexcharts";

const one = ref(0);
const two = ref(0);
const three = ref(0);
const options = ref({});
const series = ref([]);

const props = defineProps({
  msg: String,
});

const socket = io("http://localhost:3000");

socket.on("sensing data", (arg) => {
  console.log(arg);

  one.value = arg.num1; 
  two.value = arg.num2; 
  three.value = arg.num3;
  series.value = [{
    data: [
      { x: 'No.1 car', y: one.value, name: `${one.value}cm` },
      { x: 'No.2 car', y: two.value, name: `${two.value}cm` },
      { x: 'No.3 car', y: three.value, name: `${three.value}cm` }
    ]
  }];

  options.value = {
    chart: {
      height: 390,
      type: 'bar',
    },
    plotOptions: {
      bar: {
        horizontal: true,
        columnWidth: '55%',
        endingShape: 'rounded',
        dataLabels: {
          position: 'center',
          enabled: true,
          formatter: function (val) {
            return val;
          },
          offsetY: 0,
          style: {
            fontSize: '12px',
            colors: ['#000000']
          }
        }
      },
    },
    dataLabels: {
      enabled: false
    },
    xaxis: {
      max: 200,
      title: {
        text: 'cm'
      }
    },

    fill: {
      opacity: 1
    },
    tooltip: {
      y: {
        formatter: function (val) {
          return val + " cm"
        }
      }
    }
  };
});
</script>

<template>
  <div class="SENSOR">
    <h1>{{ msg }}</h1>
    <p>각 차량의 초음파 센싱 값</p>
    <div class="chart-container">
      <VueApexCharts width="500" type="bar" :options="options" :series="series" />
    </div>
    <div class="data-row">
      <div class="label">No.1: {{ one }}cm</div>
      <div class="label">No.2: {{ two }}cm</div>
      <div class="label">No.3: {{ three }}cm</div>
    </div>
  </div>
</template>

<script>
export default {
  components: {
    VueApexCharts
  }
}
</script>

<style scoped>
.SENSOR {
  text-align: center;
}

.chart-container {
  display: inline-block;
}

.data-row {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.label {
  justify-content: space-around;
  margin-right: 20px;
}
</style>

