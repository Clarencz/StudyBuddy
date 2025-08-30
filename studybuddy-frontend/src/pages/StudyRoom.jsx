import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

const StudyRoom = () => {
  const { id } = useParams(); // room id from URL
  const navigate = useNavigate();

  const [room, setRoom] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const token = localStorage.getItem("token");

  // Fetch room details
  useEffect(() => {
    const fetchRoom = async () => {
      try {
        const res = await axios.get(`http://127.0.0.1:5000/api/rooms/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setRoom(res.data.room); // backend should return { room: {...} }
      } catch (err) {
        console.error(err);
        setError("Failed to load room details.");
      } finally {
        setLoading(false);
      }
    };
    fetchRoom();
  }, [id, token]);

  // Join room
  const handleJoin = async () => {
    try {
      await axios.post(
        `http://127.0.0.1:5000/api/rooms/${id}/join`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert("You joined the room!");
      window.location.reload(); // refresh room details
    } catch (err) {
      console.error(err);
      alert("Failed to join room.");
    }
  };

  // Leave room
  const handleLeave = async () => {
    try {
      await axios.post(
        `http://127.0.0.1:5000/api/rooms/${id}/leave`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert("You left the room!");
      navigate("/rooms"); // go back to rooms list
    } catch (err) {
      console.error(err);
      alert("Failed to leave room.");
    }
  };

  if (loading) return <p>Loading room...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-2">{room.name}</h1>
      <p className="mb-2 text-gray-700">{room.description}</p>
      <p className="text-sm text-gray-500 mb-4">
        Capacity: {room.capacity} | Participants:{" "}
        {room.participants?.length || 0}
      </p>

      <div className="flex gap-3">
        <button
          onClick={handleJoin}
          className="bg-green-500 text-white px-4 py-2 rounded"
        >
          Join Room
        </button>
        <button
          onClick={handleLeave}
          className="bg-red-500 text-white px-4 py-2 rounded"
        >
          Leave Room
        </button>
      </div>

      {/* Placeholder for future features */}
      <div className="mt-6 border-t pt-4">
        <h2 className="text-xl font-semibold mb-2">Room Features</h2>
        <p className="text-gray-600">
          Whiteboard, video calls, and collaboration tools will appear here.
        </p>
      </div>
    </div>
  );
};

export default StudyRoom;
