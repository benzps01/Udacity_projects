import axios from "axios";

const baseUrl = "http://127.0.0.1:5000";

const fetchMovieDetails = async () => {
  try {
    const token = localStorage.getItem("access_token");

    const axiosConfig = {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };
    const response = await axios.get(`${baseUrl}/movies`, axiosConfig);
    return response.data["movies_dict"];
  } catch (error) {
    console.log("Error fetching data:", error);
    return [];
  }
};

export default fetchMovieDetails;
