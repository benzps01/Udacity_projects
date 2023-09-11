import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Card.css';
import UpdateActorModal from './UpdateActorModal';
import jwt_decode from 'jwt-decode';

function ActorCard(props) {
  const [selectedActor, setSelectedActor] = useState(null);
  const [canAddActor, setCanAddActor] = useState(false);
  const [canDeleteActor, setCanDeleteActor] = useState(false);
  const [canUpdateActor, setCanUpdateActor] = useState(false);

  const handleUpdateClick = (actor) => {
    setSelectedActor(actor);
  };

  const token = localStorage.getItem('access_token');

  const axiosConfig = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const handleDelete = (actor_id) => {
    axios
      .delete(
        `https://castingagency-backend.onrender.com/actors/${actor_id}`,
        axiosConfig
      )
      .then((response) => {
        console.log('Delete Successful', response.data);

        const updateActorList = props.actorDetails.filter(
          (actor) => actor.id !== actor_id
        );
        props.updateActorList(updateActorList);
      })
      .catch((error) => {
        console.log('Delete Actor', error);
      });
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      const decodedToken = jwt_decode(token);

      if (decodedToken.permissions.includes('post:actors')) {
        setCanAddActor(true);
      }
      if (decodedToken.permissions.includes('delete:actors')) {
        setCanDeleteActor(true);
      }
      if (decodedToken.permissions.includes('patch:actors')) {
        setCanUpdateActor(true);
      }
    }
  }, []);

  return (
    <>
      <div className='add-modal'>
        <button
          className='add-details'
          onClick={props.openAddActorModal}
          disabled={!canAddActor}
        >
          Add Actor
        </button>
      </div>
      {props.actorDetails.map((actor, actorIndex) => (
        <div className='card'>
          <div className='actor-content' key={actorIndex}>
            <u>Actor - Details:</u>
            <p>Name: {actor.name}</p>
            <p>Age: {actor.age}</p>
            <p>Gender: {actor.gender}</p>
          </div>
          <div className='update-modal'>
            <button
              className='update-details'
              onClick={() => handleUpdateClick(actor)}
              disabled={!canUpdateActor}
            >
              Update Actor
            </button>
          </div>
          <div className='Delete'>
            <button
              className='delete-details'
              onClick={() => handleDelete(actor.id)}
              disabled={!canDeleteActor}
            >
              Delete Actor
            </button>
          </div>
        </div>
      ))}
      {selectedActor && (
        <UpdateActorModal
          actor={selectedActor}
          onClose={() => setSelectedActor(null)}
          updateActorList={props.updateActorList}
        />
      )}
    </>
  );
}
export default ActorCard;
