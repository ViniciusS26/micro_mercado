<template>
    <div class="custom-background d-flex align-items-center">
        <div class="login-card card p-4 cadastre">
            
            <img src="../assets/logo.png" alt="Logo" class="d-block mx-auto mb-4 imagem" @error="onImageError" />
            <form @submit.prevent="login">
                <div class="mb-3 label-floating">
                    <label for="username" class="form-label cadText">Email</label>
                    <input v-model="username" type="email" class="form-control" id="username" placeholder="Digite seu email" required />
                </div>
                <div class="mb-3 label-floating">
                    <label for="password" class="form-label cadText">Senha</label>
                    <input v-model="password" type="password" class="form-control" id="password" placeholder="Digite sua senha" required />
                </div>
                <button type="submit" class="btn btn-primary w-100">Entrar</button>

                <div class="d-flex justify-content-center align-items-center mb-3">
                    <a class="text_btn" @click="resetPassword">Esqueceu a senha?</a>
                </div>
            </form>
        </div>
    </div>
</template>

  
<script setup>
import { ref } from 'vue';


const username = ref('');
const password = ref('');
const visible = ref(false);
const loading = ref(false);
const ruleEmail = (v) => /.+@.+\..+/.test(v) || /* i18n call */ 'Invalid email';

function onImageError(e) {
  e.target.src = 'https://via.placeholder.com/400x300?text=Image+Not+Found';
}
function login() {
  console.log('Login attempt with', username.value, password.value);
}
function resetPassword() {
  console.log('Reset password for', username.value);
}
</script>


<style scoped>
.custom-background {
	height: 100vh;
	background: rgb(238, 238, 238);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-family: Avenir, Helvetica, Arial, sans-serif;
    font: 700 16pt 'Open Sans', sans-serif;
}
.login-card {
    min-width: 250px !important;
    max-width: 440px !important;
    width: 60%;
    height: 50%;
    background-color: #ffffff;
    box-shadow: 0 4px 8px rgba(53, 53, 53, 0.1);
    border-radius: 8px;

}

.login-card  .imagem {
    width: 70px;
    height: auto;
    margin-bottom: 20px;
    display: block;
    margin-left: auto;
    margin-right: auto;
    margin-top: 20px;
}

.login-card h3 {
    text-align: center;
}
.btn {
    width: 100%;
    background-color: #0e3fa0;
    border: none;
    padding: 10px;
    font-size: 16px;
    margin-top: 30px;
    color: white;
    cursor: pointer;
    font-weight: bold;
    border: 1px solid #406A33;
    border-radius: 10px;
}
.btn:hover {
    background-color: #ffffff;
    color: #0e3fa0;
    cursor: pointer;
    font-weight: bold;
    border: 1px solid #0e3fa0;
    border-radius: 10px;
}
.cadastre {
    padding: 30px;
}

.cadastre .label-floating {
    border-radius: 4px;
    margin-bottom: 40px;
    height: 50px;
    width: 100%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    font-size: 20px;
}

.cadastre .label-floating  .cadText {
    color: #0e3fa0d7;
    
}
.cadastre .label-floating  input {
    border: 1px solid #0e3fa0;
    height: 40px;
    width: 100%;
    font-size: 18px;
    margin: 10px 10px 0 0;
}

.alert {
  color: red;
}
.bold {
	font-weight: bold;
	color: #0D626F;
}
a {
	cursor: pointer;
}

.textC-primary {
	color: #406A33;
	font-weight: bold;
}
</style>