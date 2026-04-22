import axios from "axios";

const API = axios.create({
 baseURL:"http://54.175.234.64:8000"
});

export const registerUser = (data)=>{
 return API.post("/register",data);
};

export const loginUser = (data)=>{
 return API.post("/login",data);
};
