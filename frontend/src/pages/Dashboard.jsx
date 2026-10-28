import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../services/api";


function Dashboard() {

    const navigate = useNavigate();

    const [user, setUser] = useState(null);


    useEffect(() => {

        const loadUser = async () => {

            try {

                const token = localStorage.getItem("token");


                const response = await api.get("/users/me");

                setUser(response.data);


            } catch(error) {

                console.log(error);

                navigate("/");

            }

        };


        loadUser();


    }, [navigate]);



    const logout = () => {

        localStorage.removeItem("token");

        navigate("/");

    };



    return (

        <div style={{ padding: "40px" }}>


            <h1>Dashboard</h1>



            {user && (

                <>

                    <h2>
                        Welcome {user.name}
                    </h2>


                    <p>
                        {user.email}
                    </p>


                </>

            )}



            <br />



            <Link to="/profile">

                <button>
                    Go To Profile
                </button>

            </Link>



            <br />
            <br />



            <button onClick={logout}>
                Logout
            </button>



        </div>

    );
}


export default Dashboard;