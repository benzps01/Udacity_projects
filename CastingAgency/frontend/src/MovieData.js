import axios from "axios";

const baseUrl = "http://127.0.0.1:5000";
const token =
  "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNfTU0xMm5FYnpmTzhicDNLeWc2ZCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmQtMTIzNC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjRmOWEzYjVkOTQ4MGIzNWIxZjRmNTJkIiwiYXVkIjoiY2FzdHMiLCJpYXQiOjE2OTQwODY0OTUsImV4cCI6MTY5NDA5MzY5NSwiYXpwIjoicFdKRnl4WTRiZ2xIWDdVWFRoT2ZuUGlmNVhxdUEyOWciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.ZzagOtiJbZmheZ3DPRLmQS5efz1VVSc6s6poTg6Iw9pvrah08uEE6rCvSEtVSI7m3_UDm3ZVTF-fxuFtRIIaFnQMKwYIfRuXJ63mYulKSkHSKsgmBSRkZ0ionQCi0R5K1_jlYowSDuw9BNCfKvdVd_3DQoXmTeexCGhxinH0wvrcWMYTV2Y8TN2wvDfULKmsy80JkxszgSxGtWO1eLnrgXCOY9-6wjtJm4XJfxdDnUdO2K9tF3Q1CzC4CXGDTvr7MwgRtY1hUGrxOm8qF3EauykW_E3hkl-DQilquPF_5lCrZQrC6f64UfAGnkEWCIk9AAnAou7EeO03HyEQG9hDLw";

const axiosConfig = {
  headers: {
    Authorization: `Bearer ${token}`,
  },
};

const fetchMovieDetails = async () => {
  try {
    const response = await axios.get(`${baseUrl}/movies`, axiosConfig);
    return response.data["movies_dict"];
  } catch (error) {
    console.log("Error fetching data:", error);
    return [];
  }
};

export default fetchMovieDetails;
