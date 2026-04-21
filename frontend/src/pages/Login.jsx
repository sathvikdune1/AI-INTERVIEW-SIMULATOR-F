import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser, registerUser } from "../api/authApi";
import "../styles/auth.css";

export default function Login() {

  const [toggled, setToggled] = useState(false);
  const navigate = useNavigate();

  const [loginData,setLoginData] = useState({
    username:"",
    password:""
  });

  const [registerData,setRegisterData] = useState({
    username:"",
    email:"",
    password:""
  });

  const handleLogin = async (e) => {
    e.preventDefault();

    try{
      const res = await loginUser(loginData);

      localStorage.setItem("token",res.data.token);
      localStorage.setItem("user",JSON.stringify(res.data.user));

      navigate("/home");

    }catch(err){
      alert("Invalid login credentials");
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    try{
      await registerUser(registerData);

      alert("Registration successful. Please login.");
      setToggled(false);

    }catch(err){
      alert("User already exists");
    }
  };

  return (

    <div className="auth-container">

      <div className={`auth-wrapper ${toggled ? "toggled" : ""}`}>

        <div className="background-shape"></div>
        <div className="secondary-shape"></div>

        {/* LOGIN */}

        <div className="credentials-panel signin">

          <h2 className="slide-element">Login</h2>

          <form onSubmit={handleLogin}>

            <div className="field-wrapper slide-element">
              <input
                type="text"
                required
                placeholder=" "
                onChange={(e)=>
                  setLoginData({...loginData,username:e.target.value})
                }
              />
              <label>Username</label>
              <i className="fa-solid fa-user"></i>
            </div>

            <div className="field-wrapper slide-element">
              <input
                type="password"
                required
                placeholder=" "
                onChange={(e)=>
                  setLoginData({...loginData,password:e.target.value})
                }
              />
              <label>Password</label>
              <i className="fa-solid fa-lock"></i>
            </div>

            <button className="submit-button slide-element" type="submit">
              Login
            </button>

            <div className="switch-link slide-element">
              <p>
                Don't have an account?
                <a
                  href="#"
                  onClick={(e)=>{
                    e.preventDefault();
                    setToggled(true);
                  }}
                >
                  Sign Up
                </a>
              </p>
            </div>

          </form>
        </div>

        {/* REGISTER */}

        <div className="credentials-panel signup">

          <h2 className="slide-element">Register</h2>

          <form onSubmit={handleRegister}>

            <div className="field-wrapper slide-element">
              <input
                type="text"
                required
                placeholder=" "
                onChange={(e)=>
                  setRegisterData({...registerData,username:e.target.value})
                }
              />
              <label>Username</label>
              <i className="fa-solid fa-user"></i>
            </div>

            <div className="field-wrapper slide-element">
              <input
                type="email"
                required
                placeholder=" "
                onChange={(e)=>
                  setRegisterData({...registerData,email:e.target.value})
                }
              />
              <label>Email</label>
              <i className="fa-solid fa-envelope"></i>
            </div>

            <div className="field-wrapper slide-element">
              <input
                type="password"
                required
                placeholder=" "
                onChange={(e)=>
                  setRegisterData({...registerData,password:e.target.value})
                }
              />
              <label>Password</label>
              <i className="fa-solid fa-lock"></i>
            </div>

            <button className="submit-button slide-element" type="submit">
              Register
            </button>

            <div className="switch-link slide-element">
              <p>
                Already have an account?
                <a
                  href="#"
                  onClick={(e)=>{
                    e.preventDefault();
                    setToggled(false);
                  }}
                >
                  Sign In
                </a>
              </p>
            </div>

          </form>
        </div>

      </div>

    </div>
  );
}