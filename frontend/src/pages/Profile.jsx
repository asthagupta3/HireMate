import { useEffect, useState } from "react";
import api from "../services/api";

function Profile() {

    const [user, setUser] = useState(null);

    const [formData, setFormData] = useState({
        name: "",
        email: ""
    });


    // Fetch profile when page loads
    useEffect(() => {

        const fetchProfile = async () => {

            try {

                const response = await api.get("/users/me");

                setUser(response.data);

                setFormData({
                    name: response.data.name,
                    email: response.data.email
                });

            } catch(error) {

                console.log(error);
            }

        };


        fetchProfile();

    }, []);



    const handleChange = (e)=>{

        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });

    };



    const updateProfile = async()=>{

        try{

            const response = await api.put(
                "/users/me",
                formData
            );


            setUser(response.data);

            alert("Profile updated successfully");


        }catch(error){

            console.log(error);
            alert("Update failed");

        }

    };



    if(!user){
        return <h2>Loading...</h2>;
    }



    return (

        <div>

            <h1>My Profile</h1>


            <div>

                <label>Name</label>

                <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                />


                <br/>


                <label>Email</label>

                <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                />


                <br/>


                <button onClick={updateProfile}>
                    Update Profile
                </button>


            </div>



            <hr/>


            <h3>User Details</h3>

            <p>
                User ID: {user.id}
            </p>


            <p>
                Name: {user.name}
            </p>


            <p>
                Email: {user.email}
            </p>


        </div>

    );
}


export default Profile;