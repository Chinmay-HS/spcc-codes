import java.io.*;
import java.util.*;

class MacroProcessor {

    static List<String> MDT = new ArrayList<>();
    static Map<String,Integer> MNT = new LinkedHashMap<>();
    static Map<String,Integer> ALA = new LinkedHashMap<>();

    public static void main(String[] args) throws Exception {

        BufferedReader br = new BufferedReader(new FileReader("input.asm"));
        List<String> output = new ArrayList<>();

        String line;
        boolean macroDef = false;
        int mdtIndex = 0;

        // -------- PASS 1 --------
        while ((line = br.readLine()) != null) {

            line = line.trim();
            if (line.isEmpty()) continue;

            if (line.equals("MACRO")) {
                macroDef = true;
                continue;
            }

            if (macroDef) {

                if (line.equals("MEND")) {
                    MDT.add("MEND");
                    macroDef = false;
                    continue;
                }

                String[] parts = line.split("\\s+");

                // First line = macro header
                if (!MNT.containsKey(parts[0])) {
                    MNT.put(parts[0], mdtIndex);

                    // build ALA
                    String[] params = parts[1].split(",");
                    for (int i = 0; i < params.length; i++) {
                        ALA.put(params[i], i);
                    }
                }

                // replace args with #index
                for (String arg : ALA.keySet()) {
                    line = line.replace(arg, "#" + ALA.get(arg));
                }

                MDT.add(line);
                mdtIndex++;
            } else {
                output.add(line);
            }
        }

        br.close();

        // -------- PRINT TABLES --------
        System.out.println("\n=== MNT ===");
        MNT.forEach((k,v)->System.out.println(k+" -> "+v));

        System.out.println("\n=== MDT ===");
        for (int i=0;i<MDT.size();i++)
            System.out.println(i+" : "+MDT.get(i));

        System.out.println("\n=== ALA ===");
        ALA.forEach((k,v)->System.out.println(k+" -> #"+v));

        // -------- PASS 2 (EXPANSION) --------
        System.out.println("\n=== EXPANDED CODE ===");

        for (String l : output) {

            String[] parts = l.split("\\s+");

            if (MNT.containsKey(parts[0])) {

                int ptr = MNT.get(parts[0]);
                String[] actuals = parts[1].split(",");

                while (!MDT.get(ptr).equals("MEND")) {

                    String temp = MDT.get(ptr);

                    for (int i = 0; i < actuals.length; i++) {
                        temp = temp.replace("#" + i, actuals[i]);
                    }

                    System.out.println(temp);
                    ptr++;
                }
            } else {
                System.out.println(l);
            }
        }
    }
}