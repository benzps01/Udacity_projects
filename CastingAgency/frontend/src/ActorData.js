import axios from "axios";

const baseUrl = "http://127.0.0.1:5000";
const token =
  "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNfTU0xMm5FYnpmTzhicDNLeWc2ZCJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWZzbmQtMTIzNC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjRmOWEzYjVkOTQ4MGIzNWIxZjRmNTJkIiwiYXVkIjoiY2FzdHMiLCJpYXQiOjE2OTQxMTAwMDEsImV4cCI6MTY5NDExNzIwMSwiYXpwIjoicFdKRnl4WTRiZ2xIWDdVWFRoT2ZuUGlmNVhxdUEyOWciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.cHSiYDbN7WjCJ3gU_QFmHqPYgK9hXIADieoL7mRHHOXDA0D1XZWtiqfF6sYjrYkfS5OHCiE38SHFuL4q0bgJs692e_2xBb41li_hGyyuW-202mmYgtABcdHP4GbkSNT3enDA0HPsljshp3tqKr7h8RRjdVujsdxPDeIBd0ZoseQtbks4-uvZV7wbyQYz8O-tzZYiF6ehqC-X35N0JGp5Eqz2QGhkthq_PYC1lgZkTdLIEzf7Qg14L8Zij4iPmnv1aESFyhKYZ6fBwWvFDkqrI6d_FFM8bwX-OskAyo7oNHBOxlnlgPLv9pICkG6SUAvN-u2NjEjGVWZp0JLhbmPn8g";

const axiosConfig = {
  headers: {
    Authorization: `Bearer ${token}`,
  },
};

const fetchActorDetails = async () => {
  try {
    const response = await axios.get(`${baseUrl}/actors`, axiosConfig);
    return response.data;
  } catch (error) {
    console.log("Error fetching data:", error);
    return [];
  }
};

export default fetchActorDetails;
