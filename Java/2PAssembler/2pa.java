import java.io.*;
import java.util.*;

class Assembler {

    static class Line {
        String l="", m="", o1="", o2="", p2="";
        int lc;
    }

    static List<Line> prog = new ArrayList<>();
    static Map<String,Integer> ST = new LinkedHashMap<>();
    static Map<String,Integer> LT = new LinkedHashMap<>();
    static Map<Integer,Integer> BT = new LinkedHashMap<>();

    static Map<String,String[]> MOT = Map.of(
        "L", new String[]{"58","4","RX"},
        "A", new String[]{"5A","4","RX"},
        "ST",new String[]{"50","4","RX"}
    );

    static Set<String> POT = Set.of("START","USING","DC","DS","END");

    public static void main(String[] args) throws Exception {

        read("input2.txt");

        seg(); mot(); pot();

        pass1(); st(); lt(); bt();

        pass2(); passTable();
    }

    // -------- PARSER --------
    static Line parse(String s){
        Line x=new Line();
        String[] p=s.trim().split("\\s+");

        if(p.length==1) x.m=p[0];
        else if(p.length==2){ x.m=p[0]; x.o1=p[1]; }
        else{
            if(MOT.containsKey(p[0])||POT.contains(p[0])){
                x.m=p[0]; x.o1=p[1]; if(p.length>2)x.o2=p[2];
            } else{
                x.l=p[0]; x.m=p[1]; x.o1=p[2]; if(p.length>3)x.o2=p[3];
            }
        }

        if(x.o1.contains(",")){
            String[] t=x.o1.split(",");
            x.o1=t[0]; x.o2=t[1];
        }
        return x;
    }

    static void read(String f)throws Exception{
        BufferedReader br=new BufferedReader(new FileReader(f));
        String s;
        while((s=br.readLine())!=null)
            if(!s.trim().isEmpty()) prog.add(parse(s));
        br.close();
    }

    // -------- TABLE PRINTS --------
    static void seg(){
        System.out.println("\n=== PROGRAM SEGREGATION ===");
        System.out.printf("%-10s %-10s %-10s %-10s\n","LABEL","MNE","OP1","OP2");
        prog.forEach(x->System.out.printf("%-10s %-10s %-10s %-10s\n",x.l,x.m,x.o1,x.o2));
    }

    static void mot(){
        System.out.println("\n=== MOT ===");
        System.out.printf("%-5s %-5s %-5s %-5s\n","MNE","OP","LEN","FMT");
        MOT.forEach((k,v)->System.out.printf("%-5s %-5s %-5s %-5s\n",k,v[0],v[1],v[2]));
    }

    static void pot(){
        System.out.println("\n=== POT ===");
        POT.forEach(System.out::println);
    }

    static void st(){
        System.out.println("\n=== SYMBOL TABLE ===");
        ST.forEach((k,v)->System.out.println(k+" -> "+v));
    }

    static void lt(){
        System.out.println("\n=== LITERAL TABLE ===");
        LT.forEach((k,v)->System.out.println(k+" -> "+v));
    }

    static void bt(){
        System.out.println("\n=== BASE TABLE ===");
        BT.forEach((k,v)->System.out.println("R"+k+" -> "+v));
    }

    // -------- PASS 1 --------
    static void pass1(){
        int lc=0;

        for(Line x:prog){

            if(x.m.equals("START")){
                lc=Integer.parseInt(x.o1);
                x.lc=lc; ST.put(x.l,lc); continue;
            }

            x.lc=lc;

            if(!x.l.isEmpty()) ST.put(x.l,lc);
            if(x.o2.startsWith("=")) LT.putIfAbsent(x.o2,-1);

            switch(x.m){
                case "USING": BT.put(Integer.parseInt(x.o2),lc); break;
                case "DC": lc+=4; break;
                case "DS":
                    int n=1;
                    String num=x.o1.replaceAll("[^0-9]","");
                    if(!num.isEmpty()) n=Integer.parseInt(num);
                    lc+=n*4; break;
                default: if(MOT.containsKey(x.m)) lc+=4;
            }
        }

        for(String k:LT.keySet()){ LT.put(k,lc); lc+=4; }
    }

    // -------- PASS 2 --------
    static void pass2(){
        int B = BT.isEmpty()?0:BT.keySet().iterator().next();

        for(Line x:prog){

            if(!MOT.containsKey(x.m)) continue;
            if(!x.o1.matches("\\d+")) continue;

            int R=Integer.parseInt(x.o1);
            int D = x.o2.startsWith("=") ? LT.getOrDefault(x.o2,0)
                    : ST.getOrDefault(x.o2,0);

            // Destination, Index, Base format
            x.p2 = "D="+D+" X=0 B="+B;
        }
    }

    // -------- FINAL PASS TABLE --------
    static void passTable(){
        System.out.println("\n=== PASS TABLE ===");
        System.out.printf("%-5s %-20s %-20s\n","LC","PASS1","PASS2");

        for(Line x:prog){
            System.out.printf("%-5d %-20s %-20s\n",
                x.lc,
                x.m+" "+x.o1+" "+x.o2,
                x.p2
            );
        }
    }
}