import axios from "axios";

const baseUrl = "https://127.0.0.1:5000/";

const fetchMovieDetails = async () => {
  try {
    const response = await axios.get(`${baseUrl}/movies`);
    return response.data;
  } catch (error) {
    console.log("Error fetching data:", error);
    return [];
  }
};

export default fetchMovieDetails;
