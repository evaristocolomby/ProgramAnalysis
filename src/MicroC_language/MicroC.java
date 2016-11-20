import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

public class MicroC {

	public static void main(String args[]) throws Exception {
            if (args.length == 0) {
                System.out.println("Error: No program specified.");
                return;
            }	
            MicroCLexer lexer = new MicroCLexer( new ANTLRFileStream(args[0]));
            MicroCParser parser = new MicroCParser(new CommonTokenStream(lexer));
            ParseTree tree = parser.stmt();
            ParseTreeWalker.DEFAULT.walk(new MicroCWalker(), tree);
        }
}
