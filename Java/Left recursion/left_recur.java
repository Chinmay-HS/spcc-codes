import java.util.*;

class NonTerminal {
    String name;
    List<String> rules = new ArrayList<>();

    NonTerminal(String name) {
        this.name = name;
    }

    void addRule(String r) {
        rules.add(r);
    }

    void print() {
        System.out.println(name + " -> " + String.join(" | ", rules));
    }
}

class Grammar {
    List<NonTerminal> nts = new ArrayList<>();

    void addRule(String input) {
        String[] parts = input.split("->");
        String name = parts[0].trim();
        NonTerminal nt = new NonTerminal(name);

        for (String r : parts[1].split("\\|")) {
            nt.addRule(r.trim());
        }

        nts.add(nt);
    }

    void solveDirect(NonTerminal A) {
        List<String> alpha = new ArrayList<>();
        List<String> beta = new ArrayList<>();

        for (String r : A.rules) {
            if (r.startsWith(A.name))
                alpha.add(r.substring(A.name.length()));
            else
                beta.add(r);
        }

        if (alpha.isEmpty()) return;

        String newName = A.name + "'";
        NonTerminal A1 = new NonTerminal(newName);

        List<String> newA = new ArrayList<>();

        for (String b : beta)
            newA.add(b + newName);

        for (String a : alpha)
            A1.addRule(a + newName);

        A1.addRule("ε");

        A.rules = newA;
        nts.add(A1);
    }

    void apply() {
        for (int i = 0; i < nts.size(); i++) {
            solveDirect(nts.get(i));
        }
    }

    void print() {
        nts.forEach(NonTerminal::print);
    }
}
class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Grammar g = new Grammar();

        System.out.print("Enter number of productions: ");
        int n = sc.nextInt();
        sc.nextLine(); 

        for (int i = 0; i < n; i++) {
            System.out.print("Enter rule: ");
            String line = sc.nextLine();
            g.addRule(line);
        }

        g.apply();

        System.out.println("\nAfter removing left recursion:");
        g.print();
    }
}