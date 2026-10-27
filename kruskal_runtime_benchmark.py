"""Benchmark Kruskal on connected, entrance-limited dungeon graphs.

Run: python kruskal_runtime_benchmark.py
Creates kruskal_runtime.csv alongside this script. No external packages needed.
Results are newly measured and may differ from previously published measurements.
"""
import csv
import math
import random
import time
from pathlib import Path


def find(parent, vertex):
    while parent[vertex] != vertex:
        parent[vertex] = parent[parent[vertex]]
        vertex = parent[vertex]
    return vertex


def union(parent, rank, roomA, roomB):
    rootA = find(parent, roomA)
    rootB = find(parent, roomB)
    if rootA == rootB:
        return False
    if rank[rootA] < rank[rootB]:
        parent[rootA] = rootB
    elif rank[rootA] > rank[rootB]:
        parent[rootB] = rootA
    else:
        parent[rootB] = rootA
        rank[rootA] += 1
    return True


def generateGraph(numRooms, maxEntrances, rng):
    if numRooms < 2 or maxEntrances < 2:
        raise ValueError('This benchmark requires at least 2 rooms and 2 entrances.')
    positions = [(rng.random() * 10000, rng.random() * 10000)
                 for _ in range(numRooms)]
    degrees = [0] * numRooms
    edges = []
    existing = set()

    def addEdge(roomA, roomB):
        distance = math.dist(positions[roomA], positions[roomB])
        edges.append((distance, roomA, roomB))
        degrees[roomA] += 1
        degrees[roomB] += 1
        existing.add((min(roomA, roomB), max(roomA, roomB)))

    # A randomized path guarantees connectivity and uses at most two entrances.
    rooms = list(range(numRooms))
    rng.shuffle(rooms)
    for i in range(numRooms - 1):
        addEdge(rooms[i], rooms[i + 1])

    # Add other possible hallways without exceeding entrance limits.
    for _ in range(numRooms * 10):
        roomA = rng.randrange(numRooms)
        roomB = rng.randrange(numRooms)
        if roomA == roomB:
            continue
        if degrees[roomA] >= maxEntrances or degrees[roomB] >= maxEntrances:
            continue
        if (min(roomA, roomB), max(roomA, roomB)) in existing:
            continue
        addEdge(roomA, roomB)
    return edges


def kruskal(numRooms, edges):
    parent = list(range(numRooms))
    rank = [0] * numRooms
    chosen = 0
    for weight, roomA, roomB in sorted(edges):
        if union(parent, rank, roomA, roomB):
            chosen += 1
            if chosen == numRooms - 1:
                break
    return chosen


def main():
    roomCounts = [100, 250, 500, 1000, 2000, 4000, 8000, 16000]
    maxEntrances = 4
    trials = 20
    rng = random.Random(42)
    output = Path(__file__).resolve().parent / 'kruskal_runtime.csv'

    with output.open('w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Rooms', 'Edges', 'Runtime (ms)', 'E log2 E'])
        for numRooms in roomCounts:
            totalTime = 0.0
            totalEdges = 0
            for _ in range(trials):
                edges = generateGraph(numRooms, maxEntrances, rng)
                startTime = time.perf_counter()
                chosen = kruskal(numRooms, edges)
                totalTime += (time.perf_counter() - startTime) * 1000
                if chosen != numRooms - 1:
                    raise RuntimeError('Kruskal did not connect every room.')
                totalEdges += len(edges)
            avgEdges = totalEdges / trials
            writer.writerow([numRooms, round(avgEdges, 2),
                             round(totalTime / trials, 6),
                             round(avgEdges * math.log2(avgEdges), 3)])
    print(f'Created {output}')
    print('Only Kruskal execution is timed; graph generation is excluded.')


if __name__ == '__main__':
    main()
