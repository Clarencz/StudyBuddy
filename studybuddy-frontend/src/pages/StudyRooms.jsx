import React, { useEffect, useState } from "react";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { PlusCircle, Users } from "lucide-react";
import { useNavigate } from "react-router-dom";

const StudyRooms = () => {
  const [rooms, setRooms] = useState([]);
  const [roomName, setRoomName] = useState("");
  const [roomDescription, setRoomDescription] = useState("");
  const [capacity, setCapacity] = useState(5);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const token = localStorage.getItem("token");

  // Fetch rooms
  const fetchRooms = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:5000/api/rooms", {
        headers: { Authorization: `Bearer ${token}` },
      });
      console.log("✅ Rooms fetched:", res.data);
      setRooms(res.data.rooms || res.data || []);
    } catch (err) {
      console.error(
        "❌ Failed to fetch rooms:",
        err.response?.data || err.message
      );
    }
  };

  useEffect(() => {
    fetchRooms();
  }, []);

  // Create new room
  const handleCreateRoom = async () => {
    if (!roomName.trim()) return;

    try {
      setLoading(true);
      const res = await axios.post(
        "http://127.0.0.1:5000/api/rooms",
        {
          name: roomName,
          description: roomDescription,
          capacity: capacity,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      console.log("✅ Room created:", res.data);

      // If backend returns the created room, add it directly
      if (res.data.room) {
        setRooms((prev) => [...prev, res.data.room]);
      } else {
        // fallback: refetch from server
        fetchRooms();
      }

      setRoomName("");
      setRoomDescription("");
      setCapacity(5);
    } catch (err) {
      console.error(
        "❌ Failed to create room:",
        err.response?.data || err.message
      );
    } finally {
      setLoading(false);
    }
  };

  // Enter room
  const handleEnterRoom = (roomId) => {
    navigate(`/study-rooms/${roomId}`);
  };

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Study Rooms</h1>

      {/* Create Room Form */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <PlusCircle className="h-5 w-5 mr-2" />
            Create a Study Room
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Input
            placeholder="Room Name"
            value={roomName}
            onChange={(e) => setRoomName(e.target.value)}
          />
          <Input
            placeholder="Room Description"
            value={roomDescription}
            onChange={(e) => setRoomDescription(e.target.value)}
          />
          <Input
            type="number"
            min="2"
            max="50"
            value={capacity}
            onChange={(e) => setCapacity(Number(e.target.value))}
          />
          <Button onClick={handleCreateRoom} disabled={loading}>
            {loading ? "Creating..." : "Create Room"}
          </Button>
        </CardContent>
      </Card>

      {/* Room List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {rooms.length > 0 ? (
          rooms.map((room) => (
            <Card key={room.id}>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Users className="h-5 w-5 mr-2" />
                  {room.name}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 mb-2">{room.description}</p>
                <p className="text-sm text-gray-500 mb-2">
                  Capacity: {room.capacity}
                </p>
                <Button onClick={() => handleEnterRoom(room.id)}>
                  Enter Room
                </Button>
              </CardContent>
            </Card>
          ))
        ) : (
          <p className="text-gray-500">No study rooms available. Create one!</p>
        )}
      </div>
    </div>
  );
};

export default StudyRooms;
