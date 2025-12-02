import React, {useEffect, useState} from 'react';

import { Navigate } from "react-router-dom";

function ProfilePage() {
  const username = localStorage.getItem("username");
  const email = localStorage.getItem("email");
  const role = localStorage.getItem("role");



  return (
    <div>
      <h1>Profile</h1>
      <p>Welcome! {username}</p>
      <p>Your email is: {email}</p>
      <p>You are a {role}.</p>
    </div>
  );
}

export default ProfilePage;