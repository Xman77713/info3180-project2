<template>

    <div class="container">
        <div className="logout-box">
            <div className="logout-header">
                <h3>Logout</h3>
                <div v-if = "logoutStatus == 'success'" class="alert alert-success">
                    <p>Successfully Logged Out</p>
                </div>
            </div>

            <div class="message-box">
                <p>Are you sure you want to logout?</p>
                <button @click="logout" class="btn btn-primary">Logout</button>
            </div>
        </div>
        
    </div>
    
    
</template>

<script setup>


  import { ref, onMounted } from "vue"; onMounted(() => {  
        getCsrfToken();   
    }); 

    import {useRouter} from "vue-router";
    const router = useRouter()

    let logoutStatus = ref("");  
    let csrf_token = ref("");

     
    let token = localStorage.getItem('token')
    
    console.log(token)

    function getCsrfToken() {     
        fetch('/api/v1/csrf-token')       
        .then((response) => response.json())       
        .then((data) => {         
            console.log(data);         
            csrf_token.value = data.csrf_token;       
        })   
    } 

    function logout() {  
        
        let auth = 'Bearer '+ token
        console.log(auth)
     
        fetch("/api/v1/auth/logout", {     
            method: 'POST',
            headers: {             
                'X-CSRFToken': csrf_token.value,
                'Authorization': auth     
                }  
            })    
        .then((response) => 
            response.json())  

        .then((data) => {         
            console.log(data); 
            if (data.hasOwnProperty('success')){
              logoutStatus.value = "success";  
              localStorage.setItem('isLogin', 'false');

              setTimeout( () => router.push({ path: '/'})
              .then(() => { router.go() }), 1000)

            }        
                
        })   
    }

     
</script>

<style>

    .container{
        display: flex;
        flex-direction: column;
        /* flex-wrap: wrap; */
        
        padding: 50px;
        
        align-items: center;
        
    }

    .logout-box{
        max-width: 500px;
        width: 100%;
    }

    .message-box{
        display: flex;
        flex-direction: column;

        justify-content: center;
        text-align: center;

        

        background-color: white;
        padding: 50px;

        box-shadow: 2px 2px 8px rgb(88, 88, 88);
    }

    .logout-header{
        margin-bottom: 15px;
    }

    h3, .message-box p{
        font-weight: bold;
    }

</style>