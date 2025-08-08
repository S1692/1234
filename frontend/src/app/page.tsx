'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface Item {
  id: number;
  name: string;
  created_at: string;
}

export default function Page() {
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE as string;
  const [items, setItems] = useState<Item[]>([]);
  const [name, setName] = useState('');
  const [health, setHealth] = useState<'loading' | 'ok' | 'fail'>('loading');

  // Fetch service health
  const fetchHealth = async () => {
    try {
      const res = await fetch(`${API_BASE}/`);
      const data = await res.json();
      if (res.ok && data?.service?.db === 'ok') {
        setHealth('ok');
      } else {
        setHealth('fail');
      }
    } catch (err) {
      setHealth('fail');
    }
  };

  // Fetch items list
  const fetchItems = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/items`);
      if (!res.ok) {
        throw new Error('Failed to fetch items');
      }
      const data: Item[] = await res.json();
      setItems(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchHealth();
    fetchItems();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Add new item
  const addItem = async () => {
    if (!name) return;
    try {
      const res = await fetch(`${API_BASE}/api/items`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name }),
      });
      if (!res.ok) {
        throw new Error('Failed to create item');
      }
      setName('');
      await fetchItems();
    } catch (err) {
      console.error(err);
    }
  };

  // Delete item by id
  const deleteItem = async (id: number) => {
    try {
      const res = await fetch(`${API_BASE}/api/items/${id}`, {
        method: 'DELETE',
      });
      if (!res.ok && res.status !== 204) {
        throw new Error('Failed to delete item');
      }
      await fetchItems();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <main className="container mx-auto p-4 max-w-4xl">
      <h1 className="text-2xl font-bold mb-4">Items</h1>

      <div className="mb-4">
        <span
          className={`px-2 py-1 rounded text-sm ${
            health === 'ok'
              ? 'bg-green-200 text-green-800'
              : health === 'fail'
              ? 'bg-red-200 text-red-800'
              : 'bg-yellow-200 text-yellow-800'
          }`}
        >
          {health === 'ok'
            ? 'DB OK'
            : health === 'fail'
            ? 'DB FAIL'
            : 'Checking...'}
        </span>
      </div>

      <div className="flex mb-4 space-x-2">
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Item name"
          className="flex-1 px-2 py-1 border rounded"
        />
        <button
          onClick={addItem}
          className="px-3 py-1 bg-blue-600 text-white rounded"
        >
          Add
        </button>
        <button
          onClick={() => {
            fetchItems();
            fetchHealth();
          }}
          className="px-3 py-1 bg-gray-600 text-white rounded"
        >
          Reload
        </button>
        <Link href="/signup" className="px-3 py-1 bg-green-600 text-white rounded flex items-center">
          Sign Up
        </Link>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border border-gray-300 text-sm">
          <thead>
            <tr className="bg-gray-100">
              <th className="border px-2 py-1 text-left">ID</th>
              <th className="border px-2 py-1 text-left">Name</th>
              <th className="border px-2 py-1 text-left">Created At</th>
              <th className="border px-2 py-1 text-left">Action</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id} className="hover:bg-gray-50">
                <td className="border px-2 py-1">{item.id}</td>
                <td className="border px-2 py-1">{item.name}</td>
                <td className="border px-2 py-1">
                  {new Date(item.created_at).toLocaleString()}
                </td>
                <td className="border px-2 py-1">
                  <button
                    onClick={() => deleteItem(item.id)}
                    className="text-red-600 hover:underline"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
