<template>
  <div>
  
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:30px">
  <h1 style="margin:0">基于Spark的心脏病风险预测系统</h1>
  <el-button type="warning" @click="changePassword">修改密码</el-button>
  <el-button type="danger" @click="logout">退出登录</el-button>
  </div>
  
  <el-card style="width:600px;margin:40px auto">
  
  <el-form :model="form" label-width="180px">
  
  <el-form-item label="年龄 Age (20-100)">
  <el-input-number v-model="form.Age" :min="20" :max="100"></el-input-number>
  </el-form-item>
  
  <el-form-item label="性别 Sex">
  <el-select v-model="form.Sex">
  <el-option label="男 Male" :value="1"></el-option>
  <el-option label="女 Female" :value="0"></el-option>
  </el-select>
  </el-form-item>
  
  <el-form-item label="胸痛类型 Chest Pain">
  <el-tooltip
  raw-content
  content="胸痛类型：指胸部疼痛的性质,是判断心绞痛的重要指标.<br>典型心绞痛 (Typical Angina):由心肌缺血引起的典型胸痛,常在运动或情绪激动时出现，休息后缓解.<br>非典型心绞痛 (Atypical Angina):与心绞痛相似,但症状不完全符合典型心绞痛.<br>非心绞痛 (Non-anginal Pain):胸痛与心脏缺血无关,可能由肌肉或消化系统引起.<br>无症状 (Asymptomatic):没有明显胸痛症状."
  placement="right">
  <el-select v-model="form.ChestPain">
  <el-option label="典型心绞痛" :value="3"></el-option>
  <el-option label="非典型心绞痛" :value="2"></el-option>
  <el-option label="非心绞痛" :value="1"></el-option>
  <el-option label="无症状" :value="0"></el-option>
  </el-select>
  </el-tooltip>
  </el-form-item>
  
  <el-form-item label="静息血压 Rest BP (80-200)">
  <el-tooltip
  raw-content
  content="静息血压（Resting Blood Pressure）是指人在安静休息状态下测量的动脉血压，通常用于评估心血管系统健康状况，血压过高可能增加心脏病和动脉硬化的风险。"
  placement="right">
  <el-input-number v-model="form.RestBP" :min="80" :max="200"></el-input-number>
  </el-tooltip>
  </el-form-item>
  
  <el-form-item label="胆固醇 Chol (100-600)">
  <el-tooltip
  raw-content
  content="胆固醇（Cholesterol）是血液中的一种脂类物质，参与细胞膜和激素合成，但如果血液胆固醇水平过高，会增加动脉粥样硬化和心血管疾病（如冠心病）的风险。"
  placement="right">
  <el-input-number v-model="form.Chol" :min="100" :max="600"></el-input-number>
  </el-tooltip>
  </el-form-item>
  
  <el-form-item label="空腹血糖 FBS">
  <el-tooltip
  raw-content
  content="空腹血糖（Fasting Blood Sugar, FBS）是指人在至少8小时未进食的情况下测量的血液葡萄糖水平。<br>≤120 mg/dl:正常或偏低<br>>120 mg/dl:偏高，可能提示糖代谢异常或糖尿病风险:"
  placement="right">
  <el-select v-model="form.Fbs">
  <el-option label="≤120 mg/dl" :value="0"></el-option>
  <el-option label=">120 mg/dl" :value="1"></el-option>
  </el-select>
  </el-tooltip>
  </el-form-item>
  
  <el-form-item label="最大心率 Max HR (60-220)">
  <el-tooltip
  raw-content
  content="最大心率是人体在递增负荷运动中，耗氧量和心率无法继续增加时达到的峰值数值"
  placement="right">
  <el-input-number v-model="form.MaxHR" :min="60" :max="220"></el-input-number>
  </el-tooltip>
  </el-form-item>
  
  <el-form-item label="静息心电图 RestECG">
  <el-tooltip
  raw-content
  content="静息心电图（Resting Electrocardiogram）是指人在安静状态下测量的心脏电活动，用于判断心脏节律和心肌是否存在异常。<br>ST-T波异常:可能提示心肌缺血<br>左心室肥厚:心脏肌肉增厚，可能由高血压引起."
  placement="right">
  <el-select v-model="form.RestECG">
  <el-option label="正常" :value="0"></el-option>
  <el-option label="ST-T异常" :value="1"></el-option>
  <el-option label="左心室肥厚" :value="2"></el-option>
  </el-select>
  </el-tooltip>
  </el-form-item>
  
  <el-form-item label="运动诱发心绞痛 ExAng">
  <el-tooltip
  raw-content
  content="运动诱发心绞痛（Exercise Induced Angina）表示患者在运动或体力活动时是否出现心绞痛症状。"
  placement="right">
  <el-select v-model="form.ExAng">
  <el-option label="否" :value="0"></el-option>
  <el-option label="是" :value="1"></el-option>
  </el-select>
  </el-tooltip>
  </el-form-item>
  
  <el-form-item label="ST下降值 Oldpeak (0-6)">
  <el-tooltip
  raw-content
  content="ST段下降值（Oldpeak）表示运动后心电图ST段相对于静息状态的下降幅度，用于评估心肌缺血程度。<br>数值越大 → 心肌缺血可能越严重."
  placement="right">
  <el-input-number v-model="form.Oldpeak" :min="0" :max="6" :step="0.1"></el-input-number>
  </el-tooltip>
  </el-form-item>
  
  <el-form-item label="ST斜率 Slope">
  <el-tooltip
  raw-content
  content="ST段斜率（Slope）是指运动后心电图ST段的变化趋势，是判断心肌缺血的重要指标。<br>下降型通常更可能提示心脏问题。"
  placement="right">
  <el-select v-model="form.Slope">
  <el-option label="上升" :value="1"></el-option>
  <el-option label="平坦" :value="2"></el-option>
  <el-option label="下降" :value="3"></el-option>
  </el-select>
  </el-tooltip>  
  </el-form-item>
  
  <el-form-item label="血管数量 Ca">
  <el-tooltip
  raw-content
  content="血管数量（Number of Major Vessels）表示通过造影检测到的主要冠状动脉狭窄数量。<br>数值越大，通常说明 冠心病风险越高。"
  placement="right">
  <el-input-number v-model="form.Ca" :min="0" :max="3"></el-input-number>
  </el-tooltip>
  </el-form-item>
  
  <el-form-item label="地中海贫血 Thal">
  <el-tooltip
  raw-content
  content="地中海贫血（Thalassemia）是一种遗传性血红蛋白疾病，该指标反映血液检查结果。<br>固定缺陷：心肌长期受损，血流问题是永久性的。<br>可逆缺陷：心肌在某些情况下血流不足，但休息时可以恢复。"
  placement="right">
  <el-select v-model="form.Thal">
  <el-option label="正常" :value="0"></el-option>
  <el-option label="固定缺陷" :value="1"></el-option>
  <el-option label="可逆缺陷" :value="2"></el-option>
  </el-select>
  </el-tooltip>
  </el-form-item>
  
  <el-form-item>
  <el-button type="primary" @click="predict">
  预测心脏病风险
  </el-button>
  </el-form-item>
  
  </el-form>
  
  <h2
  v-if="result"
  :style="{
  color: riskColor,
  textAlign:'center',
  marginTop:'20px',
  fontWeight:'bold'
  }"
  >
  预测结果：{{result}}
  </h2>
  
  <h3 v-if="risk" style="margin-top:20px">
  风险概率 Risk Probability
  </h3>
  
  <el-progress
  v-if="risk"
  :percentage="risk"
  :color="riskColor"
  style="margin-top:10px">
  </el-progress>
  
  <h3 style="margin-top:40px">历史预测记录</h3>
  <div style="overflow-x:auto">
  <el-table :data="history" style="min-width:1800px">

  <el-table-column prop="age" label="年龄"></el-table-column>
  <el-table-column label="性别"><template #default="scope">{{ scope.row.sex == 1 ? "男" : "女" }}</template></el-table-column>
  <el-table-column label="胸痛类型"><template #default="scope">{{ ["无症状","非心绞痛","非典型心绞痛","典型心绞痛"][scope.row.chestPain] }}</template></el-table-column>
  <el-table-column prop="restBP" label="静息血压"></el-table-column>
  <el-table-column prop="chol" label="胆固醇"></el-table-column>
  <el-table-column label="空腹血糖"><template #default="scope">{{ scope.row.fbs == 1 ? ">120 mg/dl" : "≤120 mg/dl" }}</template></el-table-column>
  <el-table-column prop="restECG" label="静息心电图"></el-table-column>
  <el-table-column prop="maxHR" label="最大心率"></el-table-column>
  <el-table-column label="运动诱发心绞痛"><template #default="scope">{{ scope.row.exAng == 1 ? "是" : "否" }}</template></el-table-column>
  <el-table-column prop="oldpeak" label="ST下降值"></el-table-column>
  <el-table-column prop="slope" label="ST斜率"></el-table-column>
  <el-table-column prop="ca" label="血管数量"></el-table-column>
  <el-table-column label="地中海贫血"><template #default="scope">{{ ["正常","固定缺陷","可逆缺陷"][scope.row.thal] }}</template></el-table-column>
  <el-table-column label="Result">
    <template #default="scope">
      <span v-if="scope.row.probability < 0.4" style="color:green">
      低风险
      </span>
      <span v-else-if="scope.row.probability < 0.7" style="color:orange">
      中风险
      </span>
      <span v-else style="color:red">
      高风险
      </span>
    </template>
  </el-table-column>
  <el-table-column prop="time" label="时间"></el-table-column>

  </el-table>
  </div>
  </el-card>
  
  </div>
  </template>
  
  <script>
  import axios from "axios"
  
  export default{
  
  mounted(){
  const userId = localStorage.getItem("user_id")
  if(!userId){
  this.$router.push("/")
  return
  }
  this.loadHistory()
},

  data(){
  return{
  
  form:{
  Age:50,
  Sex:1,
  ChestPain:0,
  RestBP:120,
  Chol:200,
  Fbs:0,
  RestECG:0,
  MaxHR:150,
  ExAng:0,
  Oldpeak:1,
  Slope:2,
  Ca:0,
  Thal:1
  },
  
  result:"",
  risk:null,
  history:[]
  
  }
  },
  
  computed:{
  
  riskColor(){
  
  if(this.risk < 40){
  return "#67C23A"   // 绿
  }
  else if(this.risk < 70){
  return "#E6A23C"   // 黄
  }
  else{
  return "#F56C6C"   // 红
  }
  
  }
  
  },
  
  methods:{

  changePassword(){
  const newPassword = prompt("请输入新密码")
  if(!newPassword){
  alert("密码不能为空")
  return
  }
  axios.post("http://192.168.153.130:5000/change_password",{
  user_id:localStorage.getItem("user_id"),
  password:newPassword
  }).then(res=>{
  alert("密码修改成功")
  })
 },

  logout(){
  localStorage.removeItem("user_id")
  this.$router.push("/")

  },
  loadHistory(){

  axios.get("http://192.168.153.130:5000/history",{
  params:{
  user_id:localStorage.getItem("user_id")
  }
  })
  .then(res=>{

  this.history = res.data

  })

},
  
  predict(){
  
  axios.post("http://192.168.153.130:5000/predict",{
  ...this.form,
  user_id:localStorage.getItem("user_id")
})
  .then(res=>{
  
  let p = res.data.probability
  
  this.risk = Math.round(p*100)
  
  if(p < 0.4){
  this.result = "低风险，建议保持健康生活方式"
  }
  else if(p < 0.7){
  this.result = "中风险，建议进行进一步体检"
  }
  else{
  this.result = "高风险，建议尽快就医检查"
  }
  
  })
  this.loadHistory()
  }
  
  }
  
  }
  </script>