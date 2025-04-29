import anvil.server
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io

@anvil.server.callable
def generate_receipt(receipt_data):
    """
    Génère un reçu PDF à partir des données de la commande.
    
    Args:
        receipt_data (dict): Dictionnaire contenant les informations de la commande
            et du client.
    
    Returns:
        anvil.Media: Le reçu au format PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Titre
    elements.append(Paragraph("Reçu de commande", styles['Title']))
    elements.append(Spacer(1, 20))
    
    # Informations de la commande
    elements.append(Paragraph(f"Numéro de commande: #{receipt_data['order_id']}", styles['Normal']))
    elements.append(Paragraph(f"Date: {receipt_data['date']}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Informations du client
    elements.append(Paragraph("Informations client:", styles['Heading2']))
    elements.append(Paragraph(f"Nom: {receipt_data['customer_name']}", styles['Normal']))
    elements.append(Paragraph(f"Email: {receipt_data['customer_email']}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Détails des produits
    elements.append(Paragraph("Détails de la commande:", styles['Heading2']))
    
    # Tableau des produits
    data = [['Produit', 'Description', 'Prix']]
    for product in receipt_data['products']:
        data.append([
            product['name'],
            product['description'],
            f"{product['price']} €"
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    # Total
    elements.append(Paragraph(f"Total: {receipt_data['total']} €", styles['Heading2']))
    elements.append(Spacer(1, 20))
    
    # Message de remerciement
    elements.append(Paragraph("Merci pour votre commande !", styles['Normal']))
    
    # Générer le PDF
    doc.build(elements)
    pdf_out = buffer.getvalue()
    
    return anvil.Media("application/pdf", pdf_out, f"receipt_{receipt_data['order_id']}.pdf") 