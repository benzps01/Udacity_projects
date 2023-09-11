import axios from 'axios';

const baseUrl = 'https://castingagency-backend.onrender.com';

const fetchActorDetails = async () => {
  try {
    const token = localStorage.getItem('access_token');
    const axiosConfig = {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };
    const response = await axios.get(`${baseUrl}/actors`, axiosConfig);
    return response.data;
  } catch (error) {
    console.log('Error fetching data:', error);
    return [];
  }
};

export default fetchActorDetails;
