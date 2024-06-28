const loginForm = document.querySelector('#login-form');

loginForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const email = loginForm.querySelector('#email').value;
  const password = loginForm.querySelector('#password').value;
  // Capture the current page's URL
  const currentPageUrl = window.location.href;
  console.log(currentPageUrl)
  const nextPath = new URLSearchParams(new URL(currentPageUrl).search).get('next');
  console.log(nextPath)
  axios.post('sign_in', {
    headers: {
			'Content-Type': 'application/json'
		},
    email: email,
    password: password,
    next: nextPath,  // Include the current page's URL in the request
  })
  .then((response) => {
    console.log(response);
    if (response.data.next) {
      window.location.href = response.data.next;  // Redirect to the URL from the response
    } else {
      window.location.href = '/'; // Default redirect to homepage
    }
  })
  .catch((error) => {
    console.log(error);
    alert('Invalid email or password');
  });
});




// function Email_valid() {
//   const email = document.getElementById('email').value;
//   axios.post('check_email', { email: email })
//     .then(response => {
//       const emailExists = response.data.email_exists;
//       const errorElement = document.getElementById('email-error');
//       if (emailExists) {
//         errorElement.innerText = 'Email already exists';
//       } else {
//         errorElement.innerText = '';
//       }
//     })
//     .catch(error => {
//       console.log(error);
//     });
// }

// function Email_valid() {
    
// 	const email = document.getElementById('email').value;
// 	var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
// 	if(!emailRegex.test(email)) {
//     document.getElementById('email_alert').style.color = '#DC3545';
//     document.getElementById('email_alert').innerHTML
//       = '☒ Please enter a valid email address.';
//     document.getElementById('create').disabled = true;
//     document.getElementById('create').style.opacity = (0.4);
//   }else {
//     document.getElementById('email_alert').style.color = 'green';
//     document.getElementById('email_alert').innerHTML
//       = '';
//     document.getElementById('create').disabled = false;
//     document.getElementById('create').style.opacity = (1);
//   }


// 	const data = {
// 		email:email
// 	}
	
// 	axios.post('/check_email', data,{
// 		headers: {
// 			'Content-Type': 'application/json'
// 		}
// 	})
// 	.then(response => {
//     const emailExists = response.data.email_exists;
//     const errorElement = document.getElementById('email-error');
//     if (emailExists) {
//       // errorElement.innerText = 'Email already exists';
//       document.getElementById('email_alert').style.color = '#DC3545';
//       document.getElementById('email_alert').innerHTML
//       = '☒ Email already exists.';
//       document.getElementById('create').disabled = true;
//       document.getElementById('create').style.opacity = (0.4);
//     } else {
//       document.getElementById('email_alert').style.color = 'green';
//       document.getElementById('email_alert').innerHTML
//        = '';
//       document.getElementById('create').disabled = false;
//       document.getElementById('create').style.opacity = (1);
//     }
//   })
//   .catch(error => {
//     console.log(error);
//   });
//   }




// const signupForm = document.getElementById('signup-form');
// signupForm.addEventListener('submit', (event) => {
//   event.preventDefault();
//   const username = document.getElementById('username').value;
//   const email = document.getElementById('email').value;
//   const password = document.getElementById('password').value;
//   axios.post('users/create/', {
//     username: username,
//     email: email,
//     password: password,
       
//     headers: {
//       'Content-Type': 'application/json',
//     }

//   })
//   .then((response) => {
//     if (response.data.success) {
//       window.location.href = '/'; // change the URL to the login page
//     } else {
//       window.location.href="sign_up"
//     }
//   })
//   .catch((error) => {
//     console.log(error);
//     alert('Invalid login credentials');
         
//   });
// });


















// const signupForm = document.getElementById('signup-form');
// signupForm.addEventListener('submit', (event) => {
//   event.preventDefault();
//   const username = document.getElementById('username').value;
//   const email = document.getElementById('email').value;
//   const password = document.getElementById('password').value;
//   axios.post('users/create/', {
//     username: username,
//     email: email,
//     password: password
//   },{
//       headers: {
//         'Content-Type': 'application/json',
//       }

//   })
//   .then((response) => {
//     if (response.data.success) {
//       window.location.href = '/'; // change the URL to the login page
//     } else {
//       window.location.href="sign_up"
//     }
//   })
//   .catch((error) => {
//     console.log(error);
//     alert('Invalid login credentials');
    
//   });
// });


// .then(function (response) {
//   if (response.data.success) {
//     window.location.href = '/login/'; // change the URL to the login page
//   } else {
//     // handle errors
//   }
// })
// .catch(function (error) {
//   // handle errors
// });













// import axios from 'axios';
// const form = document.getElementById('login-form');
// form.addEventListener('submit', async (event) => {
//   event.preventDefault();
//   const formData = new FormData(form);
//   const response = await axios.post('/api/token/', formData)
//   .then(function(response){
//     console.log(response.data);
//     window.location.href = '/'
//   })
//   .catch(function(error) {
//     // Handle the error
//     console.log(error);
//   });
// });

// axios.post('/api/token/', {
//     username: 'admin',
//     password: 'admin123'
//   })
//   .then(response => {
//     // Save JWT token in local storage or in memory
//     localStorage.setItem('access_token', response.data.access);
//     localStorage.setItem('refresh_token', response.data.refresh);
//   })
//   .catch(error => {
//     console.log(error);
//   });





//  import axios from 'axios';

//  const email = 'user@example.com';
//  const password = 'password';

//  axios.post('/api/token/', {
//    email: email,
//    password: password
//  })
//  .then(response => {
//    localStorage.setItem('access_token', response.data.access);
//    localStorage.setItem('refresh_token', response.data.refresh);
//  })
//  .catch(error => console.log(error));


