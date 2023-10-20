from typing import List

from base.extractor.func_extractor import FuncExtractor
from customizer.joinpoint.joinpoint import Joinpoint
from customizer.pointcut.func_signature import FuncSignature
from customizer.pointcut.pointcut import Pointcut


class Execution(Pointcut):
    """Executionポイントカット"""

    def __init__(self, signature):
        """
        Args:
            signature (FuncSignature): 関数のシグネチャ
        """
        self.func_signature: FuncSignature = signature

    def search(self, ast) -> List[Joinpoint]:
        """ポイントカットにマッチするジョインポイントを探索
        Args:
            ast (c_ast.FileAST): 構文木
        Returns:
            joinpoints (list[int]): ジョインポイント(行目)のリスト
        """
        extractor = FuncExtractor()
        extractor.visit(ast)
        joinpoints: List[Joinpoint] = []
        for func in extractor.functions:
            if func.name != self.func_signature.name:
                continue
            exec_start_line = func.definitioin_line
            exec_end_lines = [*func.get_exec_end_lines()]
            whole = (exec_start_line, func.last_line)
            for e_e_l in exec_end_lines:
                joinpoints.append(Joinpoint(exec_start_line, e_e_l, whole))
        # TODO マッチしなかった場合の処理
        return joinpoints
