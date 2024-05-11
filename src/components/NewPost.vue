<template>
    <div v-if="message != null">
        <div v-if="message['errors']" class="alert alert-danger" role="alert">
            <li v-for="error in message['errors']"> {{ error }}words </li>
        </div>
        <div v-else-if="message['message']" class="alert alert-success" role="alert">
            <p>{{ message['message']}} </p>
        </div>
        <h1 v-else class="alert alert-danger" role="alert">
            {{ message['error'] }}
        </h1>
    </div>
    <h1>New Post</h1>
    <div>
        <form @submit.prevent="submit" method="POST" id="newPostForm" enctype="multipart/form-data">
            <div class="form-group mb-3">
                <label for="photo" class="form-label">Photo</label>
                <input type="file" name="photo" class="form-control">
            </div>
            <div class="form-group mb-3">
                <label for="caption" class="form-label">Caption</label>
                <textarea type="text" class="form-control" name="caption" placeholder="Write a caption..."></textarea>
            </div>
            <button class="btn btn-primary" type="submit" id="Post">Submit</button>
        </form>
    </div>
</template>

<script setup>
    import { jwtDecode } from "jwt-decode";
    import { ref, onMounted } from "vue";    

    const csrf_token = ref(null)
    let user_id
    const message = ref(null)
    const token = ref(null)

    onMounted(() =>{
        token.value = localStorage.getItem("token")
        getCsrf();
        getUserId();
        console.log(user_id);
    });

    function getCsrf(){
        fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            csrf_token.value = data.csrf_token;
        })
    }

    function getUserId(){
        if(token.value){
            user_id = jwtDecode(token.value).user_id;
        }
    }

    function submit(){
        let newPostForm = document.getElementById('newPostForm');
        let form_data = new FormData(newPostForm);
        form_data.append("user_id", user_id)

        fetch(`/api/v1/users/${user_id}/posts`, {
            method: 'POST',
            body: form_data,
            headers: {
                'X-CSRFToken': csrf_token.value,
                'Authorization': `Bearer ${token.value}`
            }
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data){
            console.log(data)
            message.value = data
            console.log(message.value)
        })
        .catch(function (errors) {
            console.log(errors)
        });
    }
</script>

