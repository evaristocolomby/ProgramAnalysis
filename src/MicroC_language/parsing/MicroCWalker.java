import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author Evaristo
 */
public class MicroCWalker extends MicroCBaseListener {
 
    public List<MicroCProgramNode> program = new ArrayList<>();
    public Integer counter = 0;
    
    //constructor
    public MicroCWalker() {
        program.add(new MicroCProgramNode("Program", null, null, 0));
    }
    
    @Override
    public void enterAssignStmt(MicroCParser.AssignStmtContext ctx) {
        this.program.add(new MicroCProgramNode(ctx.getText(), null, null, this.counter ++));
     }

    @Override
    public void enterWhileStmt(MicroCParser.WhileStmtContext ctx) { 
        this.program.add(new MicroCProgramNode(ctx.getText(), null, null, this.counter ++));
        System.out.println(this.program.toString());
    }
}
