<template>

    <div class="container">
        
            <div class="form-box">
                <div className="login-header">
                    <h3>Login</h3>
                    <div v-if = "response_type == 'error'" class="alert alert-danger">
                        <ul>
                            <li v-for="error in response.errors">
                                {{ error }}
                            </li>
                        </ul>
                    </div>
                </div>
                <form @submit.prevent="loginUser" class="" id='loginForm'> 

                    <div className="form-group">
                        <label for="username" class="form-label bold">Username</label>
                        <input type="text" name="username" class="formcontrol" />
                    </div>

                    <div class="form-group">
                        <label for="password" class="form-label">Password</label>
                        <input type="text" name="password" class="formcontrol " />
                    </div>


                    <div>
                        <input class="button" type="submit" value="Login"/>
                    </div>


                    </form>
            </div>
            
        
    </div>

    

    

</template>

<script setup>

    import { ref, onMounted } from "vue"; onMounted(() => {     
        getCsrfToken(); 
    });
    import {useRouter} from "vue-router";
    const router = useRouter()

    let csrf_token = ref("");  
    let response = ref([]);
    let response_type = ref("");
    
    localStorage.setItem('isLogin', 'false'); 


    function getCsrfToken() {     
        fetch('/api/v1/csrf-token')       
        .then((response) => response.json())       
        .then((data) => {         
            console.log(data);         
            csrf_token.value = data.csrf_token;       
        })   
    }

    const loginUser = () =>{

        let loginForm = document.getElementById('loginForm'); 
        let form_data = new FormData(loginForm);

        

        fetch("/api/v1/auth/login", {     
            method: 'POST', 
            body: form_data,
            headers: {             
                'X-CSRFToken': csrf_token.value         
                }  
            })     
            .then(function (response) {         
                return response.json();     
            })     
            .then(function (data) {         
        
                console.log(data);

                if(data.hasOwnProperty('errors')){
                    response.value = data;
                    response_type.value = 'error';

                }   
                else{
                    response_type.value = 'success';
                    localStorage.setItem('token', data.token); 

                    localStorage.setItem('isLogin', 'true' ); 

                    router.push({ path : '/explore' })
                        .then(() => { router.go() });
                }  
            })     
            .catch(function (error) {         
                console.log(error, 'Error');     
            });

    }


</script>

<style>

    .form-box{
        max-width: 500px;
        width: 100%;
    }

    #loginForm{
        display: flex;
        flex-direction: column;

        justify-content: center;

        

        background-color: white;
        padding: 50px;

        box-shadow: 2px 2px 8px rgb(88, 88, 88);
    }

    .container{
        display: flex;
        flex-direction: column;
        /* flex-wrap: wrap; */
        
        padding: 50px;
        
        align-items: center;
        
    }

    .form-group{
        display: flex;
        margin-bottom: 15px;
        flex-direction: column;
    }

    .form-label{
        font-weight: bold;
    }

    .formcontrol{
        padding: 5px;
    }

    .button{
        background-color: rgb(7, 202, 43);
        color: white;
        font-weight: bold;

        border: none;
        border-radius: 10px;

        width: 100%;
        margin-top: 10px;
        padding: 6px;
    }

    .button:hover{
        background-color: rgb(4, 220, 44);
        color: white;
        transition: all 0.8s;
    }

    .login-header h3{
        font-weight: bold;
    }



</style>