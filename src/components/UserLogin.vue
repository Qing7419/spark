<template>

    <div style="width:300px;margin:150px auto">
    
    <h2 style="text-align:center">用户登录</h2>
    
    <el-input
    v-model="username"
    placeholder="用户名"
    style="margin-bottom:10px">
    </el-input>
    
    <el-input
    v-model="password"
    type="password"
    placeholder="密码"
    style="margin-bottom:20px">
    </el-input>
    

    <el-form-item label-width="0">
    <el-button
    type="primary"
    style="width:100%;margin-bottom:10px"
    @click="login">
    登录
    </el-button>

    <el-button
    type="success"
    style="width:100%"
    @click="register">
    注册
    </el-button>
    </el-form-item>
    

    </div>
    
    </template>
    
    <script>
    
    import axios from "axios"
    
    export default{
    
    data(){
    return{
    username:"",
    password:""
    }
    },
    
    methods:{
    
    register(){

    if(!this.username || !this.password){
    alert("请输入用户名和密码")
    return
    }

    axios.post("http://192.168.153.130:5000/register",{
    username:this.username,
    password:this.password
    })
    .then(res=>{

    if(res.data.message=="register success"){
    alert("注册成功，请登录")
    }
    else if(res.data.message=="user exists"){
    alert("用户名已存在")
    }

    })

},

    login(){

    if(!this.username || !this.password){
    alert("请输入用户名和密码")
    return
    }

    axios.post("http://192.168.153.130:5000/login",{
    username:this.username,
    password:this.password
    })
    .then(res=>{

    if(res.data.message=="login success"){

    localStorage.setItem("user_id",res.data.user_id)

    this.$router.push("/predict")

    }else{

    alert("用户名或密码错误")

    }

})

}
    

    }
    
    }
    
    </script>