import java.util.*;
import java.io.*;

class Optimizer {

    static class Instr {
        int id;
        String lhs, rhs;

        Instr(int id, String line) {
            this.id = id;
            String[] parts = line.split("=");
            lhs = parts[0].trim();
            rhs = parts[1].trim();
        }

        public String toString() {
            return lhs + " = " + rhs;
        }
    }

    // COST MODEL
    static int computeCost(List<Instr> code) {
        int cost = 0;

        for (Instr i : code) {
            String rhs = i.rhs;

            if (rhs.contains("*")) cost += 3;
            else if (rhs.contains("+")) cost += 2;
            else cost += 1;
        }

        return cost;
    }

    public static void main(String[] args) throws Exception {

        List<Instr> tac = new ArrayList<>();

        // READ FROM FILE
        BufferedReader br = new BufferedReader(new FileReader("input.txt"));
        String line;
        int id = 1;

        while ((line = br.readLine()) != null) {
            if (!line.trim().isEmpty())
                tac.add(new Instr(id++, line));
        }
        br.close();

        // ORIGINAL
        System.out.println("=== ORIGINAL CODE ===");
        tac.forEach(i -> System.out.println(i.id + ": " + i));

        int originalCost = computeCost(tac);

        // COPY PROPAGATION
        long cpStart = System.nanoTime();

        Map<String, String> map = new HashMap<>();

        for (Instr i : tac) {

            // replace variables using map
            for (String key : map.keySet()) {
                i.rhs = i.rhs.replaceAll("\\b" + key + "\\b", map.get(key));
            }

            // detect simple copy (x = y)
            if (!i.rhs.contains("+") && !i.rhs.contains("*") && !i.rhs.matches("\\d+")) {
                map.put(i.lhs, map.getOrDefault(i.rhs, i.rhs));
            }
        }

        long cpEnd = System.nanoTime();

        System.out.println("\n=== AFTER COPY PROPAGATION ===");
        tac.forEach(i -> System.out.println(i.id + ": " + i));

        // DEAD CODE ELIMINATION
        long dceStart = System.nanoTime();

        Set<String> used = new HashSet<>();
        List<Instr> optimized = new ArrayList<>();

        // assume these are final outputs
        used.add("x");
        used.add("y");
        used.add("z");
        used.add("w");

        for (int i = tac.size() - 1; i >= 0; i--) {
            Instr inst = tac.get(i);

            if (used.contains(inst.lhs)) {
                optimized.add(0, inst);

                for (String token : inst.rhs.split("[^a-zA-Z0-9]+")) {
                    if (token.matches("[a-zA-Z][a-zA-Z0-9]*")) {
                        used.add(token);
                    }
                }
            }
        }

        long dceEnd = System.nanoTime();

        // FINAL OUTPUT
        System.out.println("\n=== AFTER DEAD CODE ELIMINATION ===");
        int newId = 1;
        for (Instr i : optimized) {
            System.out.println(newId++ + ": " + i);
        }

        int optimizedCost = computeCost(optimized);

        // TIMINGS
        long totalTime = (cpEnd - cpStart) + (dceEnd - dceStart);

        System.out.println("\n=== TIMINGS ===");
        System.out.println("Copy Propagation: " + (cpEnd - cpStart) + " ns");
        System.out.println("Dead Code Elimination: " + (dceEnd - dceStart) + " ns");
        System.out.println("Total Optimization Time: " + totalTime + " ns");

        // COST COMPARISON
        System.out.println("\n=== EXECUTION COST COMPARISON ===");
        System.out.println("Original Cost: " + originalCost);
        System.out.println("Optimized Cost: " + optimizedCost);

        int saved = originalCost - optimizedCost;
        System.out.println("Cost Reduction: " + saved);

        double percent = (saved * 100.0) / originalCost;
        System.out.printf("Improvement: %.2f%%\n", percent);
    }
}