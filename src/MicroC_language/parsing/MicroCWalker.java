
import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author Evaristo
 */
public class MicroCWalker extends MicroCBaseListener {

    public List<MicroCProgramNode> program = new ArrayList<>();
    public Integer counter = 0;
    public Boolean test = true;
    public MicroCProgramNode self;
    public MicroCProgramNode currentNode;

    // Constructor.
    public MicroCWalker() {
        this.self = new MicroCProgramNode("Program", counter);
        this.self.setParent(this.self);
    }

    // + -
    @Override
    public void enterAexpr(MicroCParser.AexprContext ctx) {
        if (ctx.children.size() > 1) {
            currentNode = new MicroCProgramNode(ctx.getChild(1).getText(), this.counter++);
            currentNode.setParent(this.self);
            this.program.add(currentNode);
            if (test == true) {
                System.out.println("Aexpr current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
            }
        }
    }

    @Override
    public void enterIdentifier(MicroCParser.IdentifierContext ctx) {        
        currentNode = new MicroCProgramNode(ctx.getChild(0).getText(), this.counter++);
        currentNode.setParent(this.self);
        this.program.add(currentNode);
        if (test == true) {
            System.out.println("enterIdentifier current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
        }
    }

    @Override
    public void enterInteger(MicroCParser.IntegerContext ctx) {
        currentNode = new MicroCProgramNode(ctx.getChild(0).getText(), this.counter++);
        currentNode.setParent(this.self);
        this.program.add(currentNode);
        if (test == true) {
            System.out.println("enterInteger current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
        }
    }

    // * /
    @Override
    public void enterExpr1(MicroCParser.Expr1Context ctx) {
        if (ctx.children.size() > 1) {
            currentNode = new MicroCProgramNode(ctx.getChild(1).getText(), this.counter++);
            currentNode.setParent(this.self);
            this.program.add(currentNode);
            if (test == true) {
                System.out.println("Expr1 current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
            }            
        }
    }

    // =
    @Override
    public void enterExpr2(MicroCParser.Expr2Context ctx) {
        // Nothing to implement.
    }

    // ||
    @Override
    public void enterExpr(MicroCParser.ExprContext ctx) {
        if (ctx.children.size() > 1) {
            currentNode = new MicroCProgramNode(ctx.getChild(1).getText(), this.counter++);
            currentNode.setParent(this.self);
            this.program.add(currentNode);
            if (test == true) {
                System.out.println("enterExpr current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
            }      
        }
    }

    // &
    @Override
    public void enterBexpr1(MicroCParser.Bexpr1Context ctx) {
        if (ctx.children.size() > 1) {
            currentNode = new MicroCProgramNode(ctx.getChild(1).getText(), this.counter++);
            currentNode.setParent(this.self);
            this.program.add(currentNode);
            if (test == true) {
                System.out.println("enterBexpr1 current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
            }           
        }
    }

    // opr
    @Override
    public void enterBexpr2(MicroCParser.Bexpr2Context ctx) {
        if (ctx.children.size() > 1) {
            currentNode = new MicroCProgramNode(ctx.getChild(1).getText(), this.counter++);
            currentNode.setParent(this.self);           
            this.program.add(currentNode);
            if (test == true) {
                System.out.println("enterBexpr2 current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
            }
            this.self = currentNode;
        }
    }
    @Override public void exitBexpr2(MicroCParser.Bexpr2Context ctx) {
        this.self = this.self.getParent();
    }

    // -!
    @Override
    public void enterExprnegate(MicroCParser.ExprnegateContext ctx) {
        currentNode = new MicroCProgramNode(ctx.getChild(0).getText(), this.counter++);
        currentNode.setParent(this.self); 
        this.program.add(currentNode);
        if (test == true) {
            System.out.println("Expr1 current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
        }
    }

    @Override
    public void enterAssignStmt(MicroCParser.AssignStmtContext ctx) {
        String name;
        if (ctx.children.size() > 4) {
            name = "AssignStmtArray";
        } else {
            name = "AssignStmt";
        }
        currentNode = new MicroCProgramNode(name, this.counter++);
        currentNode.setParent(this.self);    
        this.program.add(currentNode);
        this.self = currentNode;
        if (test == true) {
            System.out.println("AssignStmtArray current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
        }
    }
    
    @Override 
    public void exitAssignStmt(MicroCParser.AssignStmtContext ctx) {
        this.self = this.self.getParent();
    }

    @Override
    public void enterContinueStmt(MicroCParser.ContinueStmtContext ctx) {
        currentNode = new MicroCProgramNode("ContinueStmt", this.counter++);
        currentNode.setParent(this.self);
        this.program.add(currentNode);
        if (test == true) {
            System.out.println("ContinueStmt current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
        }
        this.self = currentNode;
    }
    
    @Override public void exitContinueStmt(MicroCParser.ContinueStmtContext ctx) {
         this.self = this.self.getParent();
    }

    @Override
    public void enterReadStmt(MicroCParser.ReadStmtContext ctx) {
        String name;
        if (ctx.children.size() >= 4) {
            name = "ReadStmtArray";
        } else {
            name = "ReadStmt";
        }
        currentNode = new MicroCProgramNode(name, this.counter++);
        currentNode.setParent(this.self);
        this.program.add(currentNode);
        if (test == true) {
            System.out.println("ReadStmt current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
        }
        this.self = currentNode;
    }
    
    @Override public void exitReadStmt(MicroCParser.ReadStmtContext ctx) {
         this.self = this.self.getParent();
    }

    @Override
    public void enterBreakStmt(MicroCParser.BreakStmtContext ctx) {
        currentNode = new MicroCProgramNode("BreakStmt", this.counter++);
        currentNode.setParent(this.self);
        this.program.add(currentNode);
        if (test == true) {
            System.out.println("BreakStmt current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
        }
        this.self = currentNode;
    }

    @Override
    public void enterWriteStmt(MicroCParser.WriteStmtContext ctx) {
        currentNode = new MicroCProgramNode("writeStmt", this.counter++);
        currentNode.setParent(this.self);
        this.program.add(currentNode);
        if (test == true) {
            System.out.println("writeStmt current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
        }
        this.self = currentNode;
    }
    @Override public void exitWriteStmt(MicroCParser.WriteStmtContext ctx) {
        this.self = this.self.getParent();
    }

    @Override
    public void enterIfelseStmt(MicroCParser.IfelseStmtContext ctx) {
        currentNode = new MicroCProgramNode("IfelseStmt", this.counter++);
        currentNode.setParent(this.self);
        this.program.add(currentNode);
        if (test == true) {
            System.out.println("IfelseStmt current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
        }
        this.self = currentNode;
    }
    
    @Override public void exitIfelseStmt(MicroCParser.IfelseStmtContext ctx) {
        this.self = this.self.getParent();
    }

    @Override
    public void enterWhileStmt(MicroCParser.WhileStmtContext ctx) {
        currentNode = new MicroCProgramNode("WhileStmt", this.counter++);
        currentNode.setParent(this.self);
        this.program.add(currentNode);
        if (test == true) {
            System.out.println("WhileStmt current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
        }
        this.self = currentNode;
    }
    
    @Override public void exitWhileStmt(MicroCParser.WhileStmtContext ctx) {
        this.self = this.self.getParent();
    }

    @Override
    public void enterBlockStmt(MicroCParser.BlockStmtContext ctx) {
        // Nothing to implement.
    }

    @Override
    public void enterDecl(MicroCParser.DeclContext ctx) {
        String name;
        if (ctx.children.size() >= 4) {
            name = "enterDeclArray";
        } else {
            name = "enterDecl";
        }       
        currentNode = new MicroCProgramNode(name, this.counter++);
        currentNode.setParent(this.self);
        this.self = currentNode;
        this.program.add(currentNode);
        if (test == true) {
            System.out.println("enterDecl current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
        }
    }
    
    @Override public void exitDecl(MicroCParser.DeclContext ctx) { 
        this.self = this.self.getParent();
    }
    
    @Override public void enterType(MicroCParser.TypeContext ctx) { 
        currentNode = new MicroCProgramNode(ctx.getChild(0).getText(), this.counter++);
        currentNode.setParent(this.self);    
        this.program.add(currentNode);
        if (test == true) {
            System.out.println("enterType current_node name: " + currentNode.getName() + " Parent: " + currentNode.getParent().getName());
        }
    }

    @Override
    public void enterStmt(MicroCParser.StmtContext ctx) {
        // Nothing to Implement.
    }

    @Override
    public void exitProgram(MicroCParser.ProgramContext ctx) {
        // Nothing to Implement.
    }
}
